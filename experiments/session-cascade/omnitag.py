"""Deterministic, portable OmniTag session-state reference. No implicit memory."""
from dataclasses import dataclass, field
import hashlib
import json
import re

NAME = re.compile(r"^[^\W\d][\w-]{0,63}$", re.UNICODE)
TOKEN = re.compile(r"\[([^\[\]{}⛛]+)⛛\{([^{}]*)\}\]")

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def parse_tags(text, strict=False):
    if not isinstance(text, str):
        raise TypeError("text required")
    found = []
    for match in TOKEN.finditer(text):
        name, value = match.groups()
        if NAME.fullmatch(name) and len(value) <= 4096:
            found.append((name, value))
        elif strict:
            raise ValueError("invalid tag")
    if strict and TOKEN.sub("", text).strip():
        raise ValueError("unparsed text")
    return found

@dataclass
class SessionState:
    session_id: str
    message_count: int = 0
    tags: dict = field(default_factory=dict)
    events: list = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.session_id, str) or not self.session_id.strip():
            raise ValueError("invalid session ID")

    def ingest(self, role, content, tags=None):
        if role not in {"user", "assistant", "system", "tool"}:
            raise ValueError("invalid role")
        if not isinstance(content, str):
            raise TypeError("content must be text")
        if tags is not None and not isinstance(tags, dict):
            raise TypeError("tags must be mapping")
        incoming = tags or {}
        for name, value in incoming.items():
            if not isinstance(name, str) or not NAME.fullmatch(name):
                raise ValueError("invalid tag name")
            if not isinstance(value, str) or len(value) > 4096:
                raise ValueError("invalid tag value")
        event = {"seq": self.message_count + 1, "role": role,
                 "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest()}
        self.events.append(event)
        self.tags.update(incoming)
        self.message_count += 1

    def snapshot(self):
        return {"schema_version": "1.0", "session": self.session_id,
                "messages": self.message_count, "tags": dict(sorted(self.tags.items())),
                "last_event": self.events[-1] if self.events else None}

    def footer(self):
        snapshot = self.snapshot()
        checksum = hashlib.sha256(canonical(snapshot).encode("utf-8")).hexdigest()[:16]
        return f"[Msg⛛{{{self.message_count}}}↗️Σ∞] " + canonical({**snapshot, "checksum": checksum})

def replay(session_id, messages):
    state = SessionState(session_id)
    for message in messages:
        state.ingest(message["role"], message["content"], message.get("tags"))
    return state
