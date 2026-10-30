"""R2 identity: case-insensitive exact matching on current + historical identifiers. Never fuzzy."""
from __future__ import annotations

import re
from collections import defaultdict

from .loaders import EMAIL_RE, HASH_RE, PHONE_RE, USER_RE


def digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


class Identity:
    def __init__(self, users: list[dict], audit_rows: list[dict]):
        self.users = {u["user_id"]: u for u in users}
        self.emails, self.hashes, self.phones = defaultdict(set), defaultdict(set), defaultdict(set)
        for uid, u in self.users.items():
            self.emails[uid].add(u["email"].lower())
            self.hashes[uid].add(u["email_hash"].lower())
            self.phones[uid].add(digits(u["phone"]))
        for a in audit_rows:
            for v in (a["old_value"], a["new_value"]):
                if not v:
                    continue
                if a["field_name"] == "email":
                    self.emails[a["user_id"]].add(v.lower())
                elif a["field_name"] == "email_hash":
                    self.hashes[a["user_id"]].add(v.lower())
                elif a["field_name"] == "phone":
                    self.phones[a["user_id"]].add(digits(v))
        self.by_email, self.by_hash, self.by_phone = defaultdict(set), defaultdict(set), defaultdict(set)
        for uid in self.users:
            for e in self.emails[uid]:
                self.by_email[e].add(uid)
            for h in self.hashes[uid]:
                self.by_hash[h].add(uid)
            for p in self.phones[uid]:
                self.by_phone[p].add(uid)

    def resolve(self, email: str) -> list[str]:
        """Request email -> user ids (current or historical, case-insensitive exact)."""
        return sorted(self.by_email.get(email.lower(), ()))

    def users_in(self, text: str) -> set[str]:
        """Users whose identifiers appear verbatim (case-insensitive) in a record."""
        found = set()
        for e in EMAIL_RE.findall(text):
            found |= self.by_email.get(e.lower(), set())
        for h in HASH_RE.findall(text.lower()):
            found |= self.by_hash.get(h, set())
        for p in PHONE_RE.findall(text):
            found |= self.by_phone.get(digits(p), set())
        found |= {u for u in USER_RE.findall(text) if u in self.users}
        return found
