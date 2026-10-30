"""Loaders: CSV inputs, evidence manifest, and text evidence parsed into observation records.

Text evidence only (SQL, JSON, logs, TXT). PDFs and PNGs are media and are out of scope for
engine v0: they are listed so the run report can flag cases that need them (SPEC_CARD §2).
"""
from __future__ import annotations

import csv
import json
import re
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
HASH_RE = re.compile(r"\b[0-9a-f]{64}\b")
PHONE_RE = re.compile(r"\+\d[\d \-().]{6,}\d")
USER_RE = re.compile(r"\buser_\d+\b")
TRACE_RE = re.compile(r"\b((?:tr|rb)-[A-Za-z0-9\-]+)")
TS_RE = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)")
KV_RE = re.compile(r'(\w+)=(\\?"(?:[^"\\]|\\.)*?\\?"|[^\s"]+)')
JKV_RE = re.compile(r'"(\w+)":\s*"((?:[^"\\]|\\.)*)"')
SYS_KEYS = ("system", "data_store", "origin_system")
MEDIA_KINDS = ("pdf", "png")


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


@dataclass
class Record:
    """One observation unit: a SQL row, a JSON object with resource_id, a log trace group or a TXT line."""
    file_id: str
    captured_at: str          # manifest captured_at (R3 decides admissibility on this)
    kind: str
    system: str               # system name the source attaches (informational)
    text: str
    rids: list                # every resource id mentioned
    primary: dict = field(default_factory=dict)   # rid -> flattened fields of the record/line that IS that resource


def sniff(path: Path) -> str:
    head = path.read_bytes()[:64]
    if head.startswith(b"%PDF"):
        return "pdf"
    if head.startswith(b"\x89PNG"):
        return "png"
    s = head.lstrip()
    if s.startswith((b"{", b"[")):
        return "json"
    if s.startswith((b"--", b"PRAGMA", b"BEGIN", b"CREATE")):
        return "sql"
    if TS_RE.match(head.decode("utf-8", "replace")):
        return "log"
    return "text"


def flatten(obj, prefix="", out=None) -> dict:
    out = {} if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            flatten(v, k, out) if isinstance(v, (dict, list)) else out.setdefault(k, v)
            if isinstance(v, dict) and not v:
                out.setdefault(k, None)
    elif isinstance(obj, list):
        for v in obj:
            flatten(v, prefix, out)
    return out


def _clean(v: str):
    v = v.replace('\\"', '"').strip('"')
    return None if v in ("null", "None", "") else v


def parse_kv(line: str) -> dict:
    d = {}
    for k, v in JKV_RE.findall(line):
        d.setdefault(k, _clean(v))
    for k, v in KV_RE.findall(line):
        d.setdefault(k, _clean(v))
    m = re.match(r"^\S+ \| \w+ \| [\w.]+ \| [\w\-]+ \| (\w+) \|", line)
    if m:
        d.setdefault("event", m.group(1))
    return d


class Evidence:
    def __init__(self, data_dir: Path, rid_prefixes):
        alt = "|".join(sorted((re.escape(p) for p in rid_prefixes), key=len, reverse=True))
        self.rid_re = re.compile(rf"\b(?:{alt})_\d+\b")
        self.manifest = read_csv(data_dir / "evidence_files.csv")
        self.meta, self.records, self.coverage, self.raw = {}, [], {}, {}
        for m in self.manifest:
            p = data_dir / m["file_path"]
            fid = m["file_id"]
            kind = sniff(p)
            self.meta[fid] = {"kind": kind, "origin": m["origin"], "captured_at": m["captured_at"], "path": m["file_path"]}
            self.coverage[fid] = set()
            if kind in MEDIA_KINDS:
                self.raw[fid] = ""
                continue
            text = p.read_text(encoding="utf-8")
            self.raw[fid] = text.lower()
            parser = {"sql": self._sql, "json": self._json, "log": self._log}.get(kind, self._txt)
            recs = parser(text, fid, m)
            self.records += recs
            for rc in recs:
                for rid in rc.primary:
                    self.coverage[fid].add(rid.rsplit("_", 1)[0])

    # ---- parsers
    def _sql(self, text, fid, m):
        con = sqlite3.connect(":memory:")
        con.executescript(text)
        out = []
        for (t,) in con.execute("select name from sqlite_master where type='table'"):
            cur = con.execute(f'select * from "{t}"')
            cols = [c[0] for c in cur.description]
            for row in cur.fetchall():
                d = dict(zip(cols, row))
                if t == "snapshot_scope":
                    self.coverage[fid].add("system:" + str(d.get("origin_system")))
                    continue
                if isinstance(d.get("record_json"), str):
                    try:
                        d["record_json"] = json.loads(d["record_json"])
                    except ValueError:
                        pass
                flat = flatten(d)
                rtext = json.dumps(d, ensure_ascii=False)
                rids = sorted(set(self.rid_re.findall(rtext)))
                if not rids:
                    continue
                own = d.get("resource_id")
                flat["_table"] = t
                out.append(Record(fid, m["captured_at"], "sql", d.get("origin_system") or t, rtext, rids,
                                  {own: flat} if own else {}))
        con.close()
        return out

    def _json(self, text, fid, m):
        out = []

        def walk(o, ctx_sys):
            if isinstance(o, dict):
                sys_here = next((o[k] for k in SYS_KEYS if isinstance(o.get(k), str)), ctx_sys)
                if isinstance(o.get("data_store"), str):
                    self.coverage[fid].add("system:" + o["data_store"])
                if isinstance(o.get("resource_id"), str):
                    rtext = json.dumps(o, ensure_ascii=False, sort_keys=True)
                    rids = sorted(set(self.rid_re.findall(rtext)))
                    flat = flatten(o)
                    out.append(Record(fid, m["captured_at"], "json", sys_here, rtext, rids, {o["resource_id"]: flat}))
                    # nested documents that are themselves resources (search hits)
                    return
                for k, v in o.items():
                    if k.endswith(("_service", "_platform")):
                        self.coverage[fid].add("system:" + k)
                    walk(v, k if k.endswith(("_service", "_platform")) else sys_here)
            elif isinstance(o, list):
                for v in o:
                    walk(v, ctx_sys)

        walk(json.loads(text), "")
        return out

    def _log(self, text, fid, m):
        groups = {}
        for i, line in enumerate(text.splitlines()):
            t = TRACE_RE.search(line)
            groups.setdefault(t.group(1) if t else f"line{i}", []).append(line)
        out = []
        for lines in groups.values():
            gtext = "\n".join(lines)
            rids = sorted(set(self.rid_re.findall(gtext)))
            if not rids:
                continue
            primary = {}
            for ln in lines:
                kv = parse_kv(ln)
                rid = kv.get("resource_id")
                if rid and self.rid_re.fullmatch(rid):
                    primary.setdefault(rid, {}).update(kv)
            out.append(Record(fid, m["captured_at"], "log", "", gtext, rids, primary))
        return out

    def _txt(self, text, fid, m):
        out = []
        for ln in text.splitlines():
            rids = sorted(set(self.rid_re.findall(ln)))
            if not rids:
                continue
            parts = [x.strip() for x in ln.lstrip("- ").split("|")]
            prim = {}
            if len(parts) >= 6:
                prim[parts[2]] = {"system": parts[1], "record_type": parts[3], "result": parts[4], "subject_reference": parts[5]}
            out.append(Record(fid, m["captured_at"], "text", parts[1] if len(parts) > 2 else m["origin"], ln, rids, prim))
        return out

    def media_files(self):
        return [(fid, m) for fid, m in self.meta.items() if m["kind"] in MEDIA_KINDS]


# ----------------------------------------------------------------------------- media records (P4)
ENABLED_WORDS = {"healthy", "active", "enabled", "running", "continuous", "continuous sync", "live"}
DISABLED_WORDS = {"disabled", "paused", "stopped", "inactive"}
ABSENT_WORDS = {"not found", "deleted", "404", "absent", "removed"}


def media_fields(rec: dict) -> dict:
    """Flatten one model-extracted media record into the same field vocabulary as text evidence.
    Code, not the model, maps displayed statuses to state keys (R4)."""
    f = {k: v for k, v in (rec.get("identifiers") or {}).items() if v not in (None, "")}
    f["record_type"] = rec.get("record_type")
    f["_media"] = True
    for sf in rec.get("status_fields") or []:
        name = re.sub(r"\W+", "_", str(sf.get("name", "")).strip().lower()).strip("_")
        val = str(sf.get("value", "")).strip()
        if name and name not in f:
            f[name] = val
        low = val.lower()
        if low in ENABLED_WORDS or any(w in low for w in ("continuous", "healthy")):
            f.setdefault("enabled", True)
        if low in DISABLED_WORDS:
            f["enabled"] = False
        if low in ABSENT_WORDS:
            f["result"] = "NOT_FOUND"
    return f


def add_media(ev: "Evidence", fid: str, records: list[dict]) -> list[Record]:
    """Turn extracted media records into Records under the manifest captured_at (R3)."""
    m = ev.meta[fid]
    out = []
    for rec in records:
        rid = rec.get("resource_id")
        if rid and not ev.rid_re.fullmatch(rid):
            rid = None
        text = json.dumps(rec, ensure_ascii=False, sort_keys=True)
        # a media record observes only its own resource: ids printed in its side panels (e.g. "backup_9286
        # restored" inside backup_9287's activity list) belong to other records and must not be linked here
        rids = [rid] if rid else []
        r = Record(fid, m["captured_at"], "media", rec.get("system_hint") or m["origin"], text, rids,
                   {rid: media_fields(rec)} if rid else {})
        r.refs = set(rec.get("other_references") or []) | {v for v in (rec.get("identifiers") or {}).values() if v}
        r.media_fields = media_fields(rec)
        out.append(r)
        if rid:
            ev.coverage[fid].add(rid.rsplit("_", 1)[0])
    ev.records += out
    ev.raw[fid] = "\n".join(rc.text for rc in out).lower()
    return out
