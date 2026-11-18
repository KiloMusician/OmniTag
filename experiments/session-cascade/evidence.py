"""Evidence-first claim ledger and portable handoff capsules for OmniTag.

This module records declarations, not proof of external truth or authority.
"""
from dataclasses import dataclass, field
import hashlib
import json

STATES = frozenset({"proven", "denied", "unavailable", "unknown", "not_required"})
KINDS = frozenset({"observed", "inferred", "proposed"})
MAX_CLAIMS = 10000

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class Claim:
    subject: str
    predicate: str
    value: str
    source: str
    kind: str = "proposed"
    capability: str = "unknown"

    def __post_init__(self):
        for key in ("subject", "predicate", "value", "source"):
            val = getattr(self, key)
            if not isinstance(val, str) or not val.strip() or len(val) > 4096:
                raise ValueError("invalid " + key)
        if self.kind not in KINDS or self.capability not in STATES:
            raise ValueError("invalid evidence classification")

    def record(self):
        return {k: getattr(self, k) for k in
                ("subject", "predicate", "value", "source", "kind", "capability")}

@dataclass
class EvidenceLedger:
    session_id: str
    claims: list = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.session_id, str) or not self.session_id.strip():
            raise ValueError("invalid session id")

    def add(self, claim):
        if not isinstance(claim, Claim):
            raise TypeError("Claim required")
        if len(self.claims) >= MAX_CLAIMS:
            raise ValueError("claim limit exceeded")
        identity = digest(claim.record())
        if all(digest(item.record()) != identity for item in self.claims):
            self.claims.append(claim)
        return identity

    def conflicts(self):
        groups = {}
        for claim in self.claims:
            groups.setdefault((claim.subject, claim.predicate), {}).setdefault(
                claim.value, []).append(claim.record())
        return [{"subject": subject, "predicate": predicate, "alternatives": values}
                for (subject, predicate), values in sorted(groups.items())
                if len(values) > 1]

    def capsule(self):
        payload = {"schema": "omnitag.evidence.v1", "session": self.session_id,
                   "claims": [c.record() for c in self.claims],
                   "conflicts": self.conflicts()}
        return {**payload, "sha256": digest(payload)}

def verify_capsule(capsule):
    if not isinstance(capsule, dict):
        return False
    payload = {k: v for k, v in capsule.items() if k != "sha256"}
    if set(payload) != {"schema", "session", "claims", "conflicts"}:
        return False
    if payload["schema"] != "omnitag.evidence.v1":
        return False
    try:
        ledger = EvidenceLedger(payload["session"])
        if not isinstance(payload["claims"], list) or len(payload["claims"]) > MAX_CLAIMS:
            return False
        for raw in payload["claims"]:
            if not isinstance(raw, dict) or set(raw) != set(Claim.__dataclass_fields__):
                return False
            ledger.add(Claim(**raw))
        return ledger.capsule() == capsule
    except (ValueError, TypeError, KeyError, OverflowError):
        return False
