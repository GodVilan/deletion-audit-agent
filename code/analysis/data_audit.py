"""Read-only data audit for the Ghost Data Still Exists dataset.

Prints everything to stdout; writes nothing. Stdlib only (sqlite3 for the SQL
snapshots); pypdf is used for the PDF text-layer check when it is installed.
No model calls. Run from anywhere:

    python3 code/analysis/data_audit.py > scratch/audit_out.txt

The loaders and the evidence index are reused by gold_trace.py.
"""
from __future__ import annotations

import collections
import csv
import json
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "dataset"

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
HASH_RE = re.compile(r"\b[0-9a-f]{64}\b")
PHONE_RE = re.compile(r"\+\d[\d \-().]{6,}\d")
USER_RE = re.compile(r"\buser_\d+\b")
TRACE_RE = re.compile(r"\b((?:tr|rb)-[A-Za-z0-9\-]+)")
TS_RE = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)")
KEY_BEFORE_RE = r"""["']?([A-Za-z_][A-Za-z0-9_]*)["']?\s*[=:]\s*["']?"""


def read_csv(name: str) -> list[dict]:
    with open(DATA / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def case_num(cid: str) -> int:
    return int(cid.rsplit("_", 1)[1])


# ---------------------------------------------------------------- identities
@dataclass
class Identity:
    users: dict                      # uid -> current row
    emails: dict                     # uid -> {email_lower: set(origin)}
    hashes: dict                     # uid -> set
    phones: dict                     # uid -> set(raw)
    email_idx: dict                  # email_lower -> set(uid)
    hash_idx: dict
    phone_idx: dict                  # digits -> set(uid)


def load_identity() -> Identity:
    users = {r["user_id"]: r for r in read_csv("user_identities.csv")}
    emails = collections.defaultdict(dict)
    hashes = collections.defaultdict(set)
    phones = collections.defaultdict(set)
    for uid, r in users.items():
        emails[uid].setdefault(r["email"].lower(), set()).add("current")
        hashes[uid].add(r["email_hash"])
        phones[uid].add(r["phone"])
    for a in read_csv("user_audit_log.csv"):
        uid, f = a["user_id"], a["field_name"]
        for v, tag in ((a["old_value"], "historical"), (a["new_value"], "audit_new")):
            if not v:
                continue
            if f == "email":
                emails[uid].setdefault(v.lower(), set()).add(tag)
            elif f == "email_hash":
                hashes[uid].add(v)
            elif f == "phone":
                phones[uid].add(v)
    email_idx, hash_idx, phone_idx = (collections.defaultdict(set) for _ in range(3))
    for uid in emails:
        for e in emails[uid]:
            email_idx[e].add(uid)
    for uid in hashes:
        for h in hashes[uid]:
            hash_idx[h].add(uid)
    for uid in phones:
        for p in phones[uid]:
            phone_idx[digits(p)].add(uid)
    return Identity(users, emails, hashes, phones, email_idx, hash_idx, phone_idx)


def resolve_email(ident: Identity, email: str) -> tuple[str, list[str]]:
    """Return (how, [uids]) for a request email."""
    cur_exact = [u for u, r in ident.users.items() if r["email"] == email]
    if cur_exact:
        return "current_exact", cur_exact
    cur_ci = [u for u, r in ident.users.items() if r["email"].lower() == email.lower()]
    if cur_ci:
        return "current_case_insensitive", cur_ci
    hist_exact, hist_ci = set(), set()
    for a in AUDIT_ROWS:
        if a["field_name"] != "email":
            continue
        for v in (a["old_value"], a["new_value"]):
            if v == email:
                hist_exact.add(a["user_id"])
            elif v.lower() == email.lower():
                hist_ci.add(a["user_id"])
    if hist_exact:
        return "historical_exact", sorted(hist_exact)
    if hist_ci:
        return "historical_case_insensitive", sorted(hist_ci)
    return "unmatched", []


def within_edit2(a: str, b: str) -> int | None:
    """Levenshtein distance if <= 2, else None (banded DP)."""
    if abs(len(a) - len(b)) > 2:
        return None
    k = 2
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [k + 1] * len(b)
        lo, hi = max(1, i - k), min(len(b), i + k)
        for j in range(lo, hi + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        if min(cur[max(0, lo - 1):hi + 1]) > k:
            return None
        prev = cur
    return prev[-1] if prev[-1] <= k else None


# ------------------------------------------------------------------ evidence
@dataclass
class Rec:
    file_id: str
    captured_at: str           # manifest captured_at
    kind: str
    system: str                # system name the source attaches to the record
    text: str                  # raw record text
    rids: list = field(default_factory=list)
    rec_time: str = ""         # record-level timestamp, when the source has one
    rid_system: dict = field(default_factory=dict)  # rid -> system if finer than record


def sniff(path: Path) -> str:
    head = path.read_bytes()[:64]
    if head.startswith(b"%PDF"):
        return "pdf"
    if head.startswith(b"\x89PNG"):
        return "png"
    if head.startswith(b"SQLite format 3"):
        return "sqlite-binary"
    s = head.lstrip()
    if s.startswith(b"{") or s.startswith(b"["):
        return "json"
    if s.startswith((b"--", b"PRAGMA", b"BEGIN", b"CREATE")):
        return "sql-text"
    if TS_RE.match(head.decode("utf-8", "replace")):
        return "log-text"
    return "text"


def rid_regex(prefixes) -> re.Pattern:
    alt = "|".join(sorted((re.escape(p) for p in prefixes), key=len, reverse=True))
    return re.compile(rf"\b(?:{alt})_\d+\b")


SYS_KEYS = ("system", "data_store", "origin_system")


def json_records(obj, fid, cap, rid_re, ctx_sys="", ctx_key="", ctx_src=""):
    """System attribution order: own/ancestor system field > *_service/*_platform path key > file 'source'."""
    out = []
    if isinstance(obj, dict):
        own = next((obj[k] for k in SYS_KEYS if isinstance(obj.get(k), str)), "")
        sys_here = own or ctx_sys
        if not ctx_src and isinstance(obj.get("source"), str):
            ctx_src = f"source:{obj['source']}" + (f"/{obj['collection']}" if isinstance(obj.get("collection"), str) else "")
        if isinstance(obj.get("resource_id"), str):
            text = json.dumps(obj, ensure_ascii=False, sort_keys=True)
            t = next((obj[k] for k in ("observed_at", "recorded_at", "captured_at", "updated_at") if isinstance(obj.get(k), str)), "")
            out.append(Rec(fid, cap, "json", sys_here or ctx_key or ctx_src, text, sorted(set(rid_re.findall(text))), t))
            return out
        for k, v in obj.items():
            nk = k if re.search(r"(_service|_platform)$", k) else ctx_key
            out += json_records(v, fid, cap, rid_re, sys_here, nk, ctx_src)
    elif isinstance(obj, list):
        for v in obj:
            out += json_records(v, fid, cap, rid_re, ctx_sys, ctx_key, ctx_src)
    return out


def line_system(line: str) -> str:
    for pat in (r'\bsystem="?([\w.]+)', r'"service":"([\w.]+)"', r"\bfunction=([\w.]+)",
                r"\bservice=([\w.]+)", r"^\S+ \| \w+ \| ([\w.]+) \|", r"^\S+ <\d+>\d \S+ ([\w.]+) ",
                r"^\S+ \[\w+\] \[([\w.]+)\]"):
        m = re.search(pat, line)
        if m:
            return m.group(1)
    return ""


def sql_records(path, fid, cap, rid_re):
    con = sqlite3.connect(":memory:")
    con.executescript(path.read_text(encoding="utf-8"))
    out = []
    tables = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
    for t in tables:
        cur = con.execute(f'select * from "{t}"')
        cols = [d[0] for d in cur.description]
        for row in cur.fetchall():
            d = dict(zip(cols, row))
            if isinstance(d.get("record_json"), str):
                try:
                    d["record_json"] = json.loads(d["record_json"])
                except ValueError:
                    pass
            text = json.dumps(d, ensure_ascii=False)
            rids = sorted(set(rid_re.findall(text)))
            if not rids:
                continue
            sysname = d.get("origin_system") or f"table:{t}"
            out.append(Rec(fid, cap, "sql", sysname, f"[{t}] {text}", rids, d.get("updated_at") or ""))
    con.close()
    return out, tables


def log_records(path, fid, cap, rid_re):
    groups = collections.OrderedDict()
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        m = TRACE_RE.search(line)
        groups.setdefault(m.group(1) if m else f"line{i}", []).append(line)
    out = []
    for lines in groups.values():
        text = "\n".join(lines)
        rids = sorted(set(rid_re.findall(text)))
        if not rids:
            continue
        rid_sys = {}
        for ln in lines:
            for r in rid_re.findall(ln):
                rid_sys.setdefault(r, line_system(ln))
        sysname = rid_sys.get(rids[0], "") or line_system(lines[0])
        t = TS_RE.match(lines[-1])
        out.append(Rec(fid, cap, "log", sysname, text, rids, t.group(1) if t else "", rid_sys))
    return out


def pdf_text(path: Path) -> str | None:
    try:
        import pypdf  # optional
    except ImportError:
        return None
    return "\n".join((p.extract_text() or "") for p in pypdf.PdfReader(str(path)).pages)


def build_index(rid_prefixes):
    rid_re = rid_regex(rid_prefixes)
    manifest = read_csv("evidence_files.csv")
    recs, meta = [], {}
    for m in manifest:
        p = DATA / m["file_path"]
        fid, cap = m["file_id"], m["captured_at"]
        kind = sniff(p)
        info = {"kind": kind, "origin": m["origin"], "captured_at": cap, "path": m["file_path"], "note": ""}
        if kind == "sql-text":
            rs, tables = sql_records(p, fid, cap, rid_re)
            info["note"] = "tables=" + ",".join(tables)
        elif kind == "json":
            rs = json_records(json.loads(p.read_text(encoding="utf-8")), fid, cap, rid_re)
        elif kind == "log-text":
            rs = log_records(p, fid, cap, rid_re)
        elif kind == "pdf":
            t = pdf_text(p)
            if t is None:
                info["note"] = "text layer: unknown (pypdf not installed)"
                rs = []
            else:
                info["note"] = f"text layer: {'yes' if t.strip() else 'NO'} ({len(t)} chars)"
                rids = sorted(set(rid_re.findall(t)))
                rs = [Rec(fid, cap, "pdf", m["origin"], t, rids)] if t.strip() else []
        elif kind == "png":
            rs = []
            info["note"] = "image (not parsed)"
        else:
            rs = []
            for ln in p.read_text(encoding="utf-8").splitlines():
                rids = sorted(set(rid_re.findall(ln)))
                if rids:
                    parts = [x.strip() for x in ln.lstrip("- ").split("|")]
                    sysname = parts[1] if len(parts) > 2 else m["origin"]
                    rs.append(Rec(fid, cap, "text", sysname, ln, rids, parts[0] if parts else ""))
        info["n_records"] = len(rs)
        meta[fid] = info
        recs += rs
    return recs, meta, rid_re


def record_links(rec: Rec, ident: Identity):
    """Return {uid: set(link descriptions)} for identifiers found in the record."""
    links = collections.defaultdict(set)
    text = rec.text

    def key_for(value):
        m = re.search(KEY_BEFORE_RE + re.escape(value), text)
        return m.group(1) if m else "free_text"

    for e in set(EMAIL_RE.findall(text)):
        for u in ident.email_idx.get(e.lower(), ()):
            links[u].add(f"email({key_for(e)})")
    for h in set(HASH_RE.findall(text)):
        for u in ident.hash_idx.get(h, ()):
            links[u].add(f"email_hash({key_for(h)})")
    for ph in set(PHONE_RE.findall(text)):
        for u in ident.phone_idx.get(digits(ph), ()):
            links[u].add(f"phone({key_for(ph)})")
    for u in set(USER_RE.findall(text)):
        if u in ident.users:
            links[u].add(f"user_id({key_for(u)})")
    return links


AUDIT_ROWS = read_csv("user_audit_log.csv")


# ------------------------------------------------------------------- main
def main():
    out = sys.stdout
    P = lambda *a: print(*a, file=out)  # noqa: E731

    files = ["deletion_requests.csv", "sample_deletion_requests.csv", "sample_output.csv",
             "user_identities.csv", "user_audit_log.csv", "system_activity.csv",
             "deletion_rules.csv", "evidence_files.csv", "output.csv"]
    tables = {f: read_csv(f) for f in files}
    reqs, sreqs = tables["deletion_requests.csv"], tables["sample_deletion_requests.csv"]
    acts = tables["system_activity.csv"]
    ident = load_identity()

    # ---------------- a
    P("=" * 100)
    P("a. PER-CSV ROW COUNTS, BLANK FIELDS, DUPLICATE IDS")
    P("=" * 100)
    for f, rows in tables.items():
        with open(DATA / f, newline="", encoding="utf-8") as fh:
            header = next(csv.reader(fh))
        idcol = header[0]
        ids = [r[idcol] for r in rows]
        dups = [k for k, v in collections.Counter(ids).items() if v > 1]
        blanks = {c: sum(1 for r in rows if (r.get(c) or "") == "") for c in header}
        P(f"{f}: rows={len(rows)} id_col={idcol} unique_ids={len(set(ids))} duplicate_ids={dups or 'none'}")
        P(f"   blank fields per column: {blanks}")
    for name, rows in (("deletion_requests.csv", reqs), ("sample_deletion_requests.csv", sreqs)):
        nums = [case_num(r["case_id"]) for r in rows]
        contiguous = sorted(nums) == list(range(min(nums), max(nums) + 1))
        lex = sorted(r["case_id"] for r in rows) == [r["case_id"] for r in rows]
        lo = min(rows, key=lambda r: case_num(r["case_id"]))["case_id"]
        hi = max(rows, key=lambda r: case_num(r["case_id"]))["case_id"]
        P(f"{name}: case_id range {lo}..{hi} zero_padded={any(r['case_id'].split('_')[1].startswith('0') for r in rows)} contiguous={contiguous} "
          f"input_order==numeric_order={nums == sorted(nums)} input_order==lexicographic_order={lex}")
    P(f"reported_status (test): {dict(collections.Counter(r['reported_status'] for r in reqs))}")
    P(f"reported_status (sample): {dict(collections.Counter(r['reported_status'] for r in sreqs))}")
    P(f"gold deletion_status (sample): {dict(collections.Counter(r['deletion_status'] for r in tables['sample_output.csv']))}")
    P(f"user_audit_log field_name: {dict(collections.Counter(r['field_name'] for r in AUDIT_ROWS))}")
    P(f"evidence extensions: {dict(collections.Counter(Path(r['file_path']).suffix for r in tables['evidence_files.csv']))}")
    P(f"time-order checks: requested_at<=reported_at<=audit_at violations (test): "
      f"{[r['case_id'] for r in reqs if not (r['requested_at'] <= r['reported_at'] <= r['audit_at'])]}")
    P(f"   (sample): {[r['case_id'] for r in sreqs if not (r['requested_at'] <= r['reported_at'] <= r['audit_at'])]}")

    # ---------------- b
    P()
    P("=" * 100)
    P("b. IDENTITY RESOLUTION")
    P("=" * 100)
    all_req = [("sample", r) for r in sreqs] + [("test", r) for r in reqs]
    all_emails = {}  # email_lower -> set(uid)
    for uid, em in ident.emails.items():
        for e in em:
            all_emails.setdefault(e, set()).add(uid)
    totals = collections.Counter()
    resolved = {}
    rows_b = []
    for split, r in all_req:
        how, uids = resolve_email(ident, r["email"])
        totals[(split, how)] += 1
        if len(uids) > 1:
            totals[(split, "AMBIGUOUS_multiple_users")] += 1
        resolved[r["case_id"]] = uids
        decoys = []
        el = r["email"].lower()
        for e, us in all_emails.items():
            others = us - set(uids)
            if not others or e == el:
                continue
            d = within_edit2(el, e)
            if d is not None:
                decoys.append(f"{e}(d={d};{','.join(sorted(others))})")
        rows_b.append((split, r["case_id"], r["email"], how, uids, decoys))
    P("Totals:")
    for k in sorted(totals):
        P(f"   {k[0]:6s} {k[1]:32s} {totals[k]}")
    P(f"   test emails containing uppercase: {sum(1 for r in reqs if r['email'] != r['email'].lower())}; "
      f"sample: {sum(1 for r in sreqs if r['email'] != r['email'].lower())}")
    P(f"   requests with >=1 decoy candidate (edit distance <=2 to another user's email): "
      f"sample={sum(1 for x in rows_b if x[0]=='sample' and x[5])} test={sum(1 for x in rows_b if x[0]=='test' and x[5])}")
    P()
    P("Per request: split case_id email -> how [uids] | decoy candidates")
    for split, cid, em, how, uids, decoys in rows_b:
        P(f"   {split:6s} {cid:9s} {em} -> {how} {uids} | decoys: {'; '.join(decoys) or '-'}")
    P()
    P("Per resolved user: all current+historical emails / email_hashes / phones")
    for uid in sorted({u for us in resolved.values() for u in us}, key=lambda u: int(u.split('_')[1])):
        em = "; ".join(f"{e}[{'/'.join(sorted(t))}]" for e, t in sorted(ident.emails[uid].items()))
        P(f"   {uid}: emails={em}")
        P(f"      hashes={sorted(ident.hashes[uid])}")
        P(f"      phones={sorted(ident.phones[uid])}")

    # ---------------- c
    rid_prefixes = sorted({a["resource_id"].rsplit("_", 1)[0] for a in acts})
    recs, meta, rid_re = build_index(rid_prefixes)
    P()
    P("=" * 100)
    P("c. EVIDENCE INVENTORY")
    P("=" * 100)
    P(f"resource_id prefixes (derived from system_activity.resource_id): {rid_prefixes}")
    P(f"total parsed evidence records carrying a resource_id: {len(recs)}")
    by_file = collections.defaultdict(list)
    for rc in recs:
        by_file[rc.file_id].append(rc)
    P(f"sniffed types: {dict(collections.Counter(m['kind'] for m in meta.values()))}")
    for fid, m in meta.items():
        rs = by_file.get(fid, [])
        systems = collections.Counter(rc.system for rc in rs)
        for rc in rs:
            for s in rc.rid_system.values():
                if s:
                    systems[s] += 0
        rids = {x for rc in rs for x in rc.rids}
        prefixes = collections.Counter(x.rsplit("_", 1)[0] for x in rids)
        linktypes = collections.Counter()
        for rc in rs:
            for ls in record_links(rc, ident).values():
                for l in ls:
                    linktypes[l] += 1
        P(f"{fid} [{m['kind']}] {m['path']} origin={m['origin']} captured_at={m['captured_at']} {m['note']}")
        P(f"    records={len(rs)} distinct_resource_ids={len(rids)} prefixes={dict(prefixes)}")
        P(f"    systems named={dict(systems)}")
        P(f"    user-link identifier types (type(field): count)={dict(linktypes)}")

    # ---------------- d
    P()
    P("=" * 100)
    P("d. SYSTEM_ACTIVITY")
    P("=" * 100)
    results = sorted({a["reported_result"] for a in acts})
    ct = collections.Counter((a["event_type"], a["reported_result"]) for a in acts)
    P(f"{'event_type':24s} " + " ".join(f"{r:>9s}" for r in results) + "     total")
    for et in sorted({a["event_type"] for a in acts}):
        row = [ct[(et, r)] for r in results]
        P(f"{et:24s} " + " ".join(f"{v:9d}" for v in row) + f" {sum(row):9d}")
    P()
    P("resource_id prefix -> target_system (count)   [source_system (count)]")
    pm = collections.defaultdict(collections.Counter)
    ps = collections.defaultdict(collections.Counter)
    for a in acts:
        pm[a["resource_id"].rsplit("_", 1)[0]][a["target_system"]] += 1
        ps[a["resource_id"].rsplit("_", 1)[0]][a["source_system"]] += 1
    for p in sorted(pm):
        P(f"   {p:15s} -> {dict(pm[p])}   [{dict(ps[p])}]")
    for et in ("LINK_RESOURCE_IDENTITY", "RESTORE_BACKUP", "CLASSIFY_REQUEST"):
        P()
        P(f"--- every {et} row")
        for a in acts:
            if a["event_type"] == et:
                P("   " + ",".join(a[k] for k in a))
    P()
    P(f"activity event_time range: {min(a['event_time'] for a in acts)} .. {max(a['event_time'] for a in acts)}; "
      f"input sorted by activity number == sorted by event_time: "
      f"{[a['activity_id'] for a in acts] == [a['activity_id'] for a in sorted(acts, key=lambda a: a['event_time'])]}")

    # ---------------- e
    P()
    P("=" * 100)
    P("e. REQUEST_TEXT")
    P("=" * 100)
    alltexts = [(r["case_id"], r["request_text"], "test") for r in reqs] + [(r["case_id"], r["request_text"], "sample") for r in sreqs]
    P(f"distinct request_text: test={len({t for _, t, s in alltexts if s=='test'})} "
      f"sample={len({t for _, t, s in alltexts if s=='sample'})} union={len({t for _, t, _ in alltexts})}")
    del_kw = re.compile(
        r"delet|eras|remov|close (?:my|this|the) account|closing my account|permanent|erasure|forget|"
        r"supprim|suppression|effac|eliminar|eliminación|borrar|löschen|lösch|entfern|cancellare|eliminare|"
        r"excluir|exclusão|apagar|verwijder|usuń|usunię|削除|삭제|删除|注销|退会|탈퇴|удал|sil", re.I)
    neg_kw = re.compile(
        r"\bnot\b[^.]{0,40}\b(?:delet|eras|remov|close)|don't|do not|isn't|without (?:delet|remov|eras)|no deletion|"
        r"marketing[^.]{0,20}\bonly\b|"
        r"\bne\b[^.]{0,20}\bpas\b|\bno\b[^.]{0,20}(?:elimin|borr)|nicht|kein|ではありません|しないで|않|아니", re.I)
    other_intent = re.compile(
        r"\bcopy\b|access|export|download|correct|update|change my|opt[- ]?out|unsubscrib|marketing|newsletter|"
        r"rectif|copia|portab|kopie|berichtig|abmeld|コピー|訂正|사본|수정", re.I)
    flagged = []
    for cid, t, s in alltexts:
        reasons = []
        if not del_kw.search(t):
            reasons.append("no-deletion-keyword")
        if neg_kw.search(t):
            reasons.append("negation")
        if other_intent.search(t) and reasons:
            reasons.append("other-intent-keyword")
        if reasons:
            flagged.append((s, cid, reasons, t))
    P(f"heuristic flags (no deletion keyword OR negation pattern): {len(flagged)} requests")
    for s, cid, reasons, t in flagged:
        P(f"   {s:6s} {cid} {reasons}\n      {t}")
    classify = [a for a in acts if a["event_type"] == "CLASSIFY_REQUEST"]
    P(f"CLASSIFY_REQUEST rows: {len(classify)} (see section d)")
    P()
    P("All distinct request_text values with counts and case_ids (test+sample):")
    groups = collections.defaultdict(list)
    for cid, t, s in alltexts:
        groups[t].append(cid)
    for t, cids in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        show = cids if len(cids) <= 6 else cids[:6] + [f"...+{len(cids)-6}"]
        P(f"   [{len(cids):3d}] {show} :: {t}")

    # ---------------- f
    P()
    P("=" * 100)
    P("f. SAMPLE/TEST OVERLAP")
    P("=" * 100)
    s_em = {r["email"].lower(): r["case_id"] for r in sreqs}
    t_em = collections.defaultdict(list)
    for r in reqs:
        t_em[r["email"].lower()].append(r["case_id"])
    both = sorted(set(s_em) & set(t_em))
    P(f"same email (case-insensitive) in sample and test: {len(both)}")
    for e in both:
        P(f"   {e}: sample {s_em[e]} / test {t_em[e]}")
    s_u = collections.defaultdict(list)
    t_u = collections.defaultdict(list)
    for r in sreqs:
        for u in resolved[r["case_id"]]:
            s_u[u].append(r["case_id"])
    for r in reqs:
        for u in resolved[r["case_id"]]:
            t_u[u].append(r["case_id"])
    bu = sorted(set(s_u) & set(t_u))
    P(f"same resolved user_id in sample and test: {len(bu)}")
    for u in bu:
        P(f"   {u}: sample {s_u[u]} / test {t_u[u]}")
    dup_t = {u: c for u, c in t_u.items() if len(c) > 1}
    dup_e = {e: c for e, c in t_em.items() if len(c) > 1}
    P(f"test: users with >1 request: {len(dup_t)} {dict(list(dup_t.items())[:20])}")
    P(f"test: emails with >1 request: {len(dup_e)} {dict(list(dup_e.items())[:20])}")

    # ---------------- g
    P()
    P("=" * 100)
    P("g. DELETION_RULES CATEGORY COVERAGE")
    P("=" * 100)
    family = {  # obvious system/resource family per category (analysis aid only)
        "USER_PROFILE": ("account", "account_service"),
        "SECONDARY_IDENTIFIER": ("secondary", "secondary_identifier"),
        "SEARCH_INDEX_ENTRY": ("search", "search_service"),
        "CACHE_ENTRY": ("cache", "cache_service"),
        "SUPPORT_MESSAGE": ("support", "support_platform"),
        "SUPPORT_ATTACHMENT": ("object", "object_storage"),
        "ANALYTICS_PROFILE": ("analytics", "analytics_platform"),
        "PRODUCT_TELEMETRY": ("telemetry", "telemetry"),
        "USER_EXPORT": ("export", "export_service"),
        "MARKETING_PROFILE": ("marketing", "marketing_platform"),
        "EMAIL_DELIVERY_LOG": ("email_delivery", "email_delivery_service"),
        "SECURITY_AUDIT_LOG": ("audit_record", "security_service"),
        "LEGAL_HOLD_RECORD": ("legal_hold", "legal_service"),
        "BACKUP_ARCHIVE": ("backup", "backup_service"),
        "ACCOUNT_TOMBSTONE": ("tombstone", "identity_service"),
    }
    raw_text = {}
    for m in tables["evidence_files.csv"]:
        p = DATA / m["file_path"]
        if meta[m["file_id"]]["kind"] == "pdf":
            raw_text[m["file_id"]] = pdf_text(p) or ""
        elif meta[m["file_id"]]["kind"] != "png":
            raw_text[m["file_id"]] = p.read_text(encoding="utf-8")
    for rule in tables["deletion_rules.csv"]:
        cat = rule["data_category"]
        pref, sysname = family[cat]
        lit = [f for f, t in raw_text.items() if cat in t]
        lit_act = [a["activity_id"] for a in acts if cat in a["details"]]
        prefre = re.compile(rf"\b{re.escape(pref)}_\d+\b")
        fam = [f for f, t in raw_text.items() if prefre.search(t) or sysname in t]
        fam_act = collections.Counter(a["event_type"] for a in acts
                                      if a["resource_id"].startswith(pref + "_") or sysname in (a["target_system"], a["source_system"]))
        png = [m["file_id"] for m in tables["evidence_files.csv"]
               if meta[m["file_id"]]["kind"] == "png" and (pref in m["file_path"] or sysname == m["origin"])]
        P(f"{rule['rule_id']} {cat} -> {rule['required_action']} ({rule['condition']})")
        P(f"    literal '{cat}' in evidence files: {lit or 'none'}")
        P(f"    literal '{cat}' in activity details: {len(lit_act)} {lit_act[:5]}")
        P(f"    family '{pref}_N' / '{sysname}' in evidence files: {fam or 'none'}")
        P(f"    family in activity (event_type counts): {dict(fam_act) or 'none'}")
        P(f"    PNG candidates by filename/origin (unparsed): {png or 'none'}")

    # ---------------- z (spec-card checks)
    P()
    P("=" * 100)
    P("z. SPEC-CARD CHECKS")
    P("=" * 100)
    sout = {r["case_id"]: json.loads(r["steps_json"]) for r in tables["sample_output.csv"]}
    sreq = {r["case_id"]: r for r in sreqs}
    capt = {m["file_id"]: m["captured_at"] for m in tables["evidence_files.csv"]}
    eq, after = [], []
    for cid, steps in sout.items():
        for s in steps:
            e = s["evidence_id"]
            if e in capt:
                if capt[e] == sreq[cid]["audit_at"]:
                    eq.append(f"{cid}:{e}")
                if capt[e] > sreq[cid]["audit_at"]:
                    after.append(f"{cid}:{e}")
    P(f"sample cited files with captured_at == audit_at: {sorted(set(eq))}")
    P(f"sample cited files with captured_at > audit_at: {sorted(set(after)) or 'none'}")
    cited_kinds = collections.Counter(s["evidence_id"].split("_")[0] for st in sout.values() for s in st if s["evidence_id"])
    P(f"sample cited evidence id kinds: {dict(cited_kinds)}")
    P(f"sample cited file_ids per case: " + "; ".join(
        f"{c}:{sorted({s['evidence_id'] for s in st if s['evidence_id']})}" for c, st in sout.items()))
    ser = collections.defaultdict(list)
    for r in tables["sample_output.csv"]:
        st = json.loads(r["steps_json"])
        if r["steps_json"] == json.dumps(st, sort_keys=True, separators=(",", ":"), ensure_ascii=False):
            ser["compact, sorted keys"].append(r["case_id"])
        elif r["steps_json"] == json.dumps(st, separators=(",", ":"), ensure_ascii=False):
            ser["compact, schema key order (step_no first)"].append(r["case_id"])
        else:
            ser["other"].append(r["case_id"])
    for k, v in ser.items():
        P(f"sample steps_json serialization {k}: {len(v)} {v}")
    P(f"max steps per sample case: {max(len(s) for s in sout.values())}; step count distribution: "
      f"{dict(sorted(collections.Counter(len(s) for s in sout.values()).items()))}")


if __name__ == "__main__":
    main()
