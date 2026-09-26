#!/usr/bin/env python3
"""Validate OmniTag's public agent/human surface with stdlib only."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BEACON_PATH = ROOT / "omnitag.agent-beacon.json"
SCHEMA_PATH = ROOT / "schemas" / "agent-beacon.schema.json"
EXAMPLE_PATH = ROOT / "examples" / "arrival-receipt.json"

EXPECTED_CAPABILITY_STATES = {
    "proven",
    "denied",
    "unavailable",
    "unknown",
    "not_required",
}

REQUIRED_INVARIANTS = {
    "symbol != authority",
    "description != execution",
    "presence != proof",
    "reachable != authorized",
    "proposal != merge",
    "map != territory",
    "unknown > guessing",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def require_file(relative: str) -> None:
    path = ROOT / relative
    if not path.is_file():
        raise AssertionError(f"missing advertised entrypoint: {relative}")


def main() -> int:
    beacon = load_json(BEACON_PATH)
    load_json(SCHEMA_PATH)
    example = load_json(EXAMPLE_PATH)

    if beacon.get("schema") != "omnitag.public-agent-beacon/v1":
        raise AssertionError("unexpected beacon schema")
    if beacon.get("authority_effect") != "none":
        raise AssertionError("public beacon must not claim authority")
    if beacon.get("project", {}).get("visibility") != "public":
        raise AssertionError("public beacon must describe a public surface")

    observed_states = set(beacon.get("capability_states", []))
    if observed_states != EXPECTED_CAPABILITY_STATES:
        raise AssertionError(
            f"capability state drift: expected {sorted(EXPECTED_CAPABILITY_STATES)}, "
            f"got {sorted(observed_states)}"
        )

    observed_invariants = set(beacon.get("memory_capsule", {}).get("invariants", []))
    missing = REQUIRED_INVARIANTS - observed_invariants
    if missing:
        raise AssertionError(f"beacon is missing invariants: {sorted(missing)}")

    entrypoints = beacon.get("entrypoints", {})
    for key in ("human", "agent", "protocol", "contributing", "schema", "example"):
        relative = entrypoints.get(key)
        if not isinstance(relative, str) or not relative:
            raise AssertionError(f"missing entrypoint value: {key}")
        require_file(relative)

    if example.get("authority_effect") != "none":
        raise AssertionError("example receipt must not claim authority")

    for relative in ("README.md", "AGENTS.md", "CONTRIBUTING.md", "SECURITY.md"):
        require_file(relative)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for invariant in REQUIRED_INVARIANTS:
        if invariant not in readme and invariant not in agents:
            raise AssertionError(f"public docs lost invariant: {invariant}")

    print(
        json.dumps(
            {
                "status": "ok",
                "schema": beacon["schema"],
                "authority_effect": beacon["authority_effect"],
                "entrypoint_count": len(entrypoints),
                "capability_states": sorted(observed_states),
                "invariant_count": len(observed_invariants),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
