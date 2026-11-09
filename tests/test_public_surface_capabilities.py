"""Regression tests for capability-state uniqueness in the public validator."""

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_public_surface.py"
spec = importlib.util.spec_from_file_location("public_surface_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class CapabilityStateTests(unittest.TestCase):
    def check_states(self, states):
        beacon = {
            "schema": "omnitag.public-agent-beacon/v1",
            "authority_effect": "none",
            "project": {"visibility": "public"},
            "capability_states": states,
            "memory_capsule": {"invariants": sorted(validator.REQUIRED_INVARIANTS)},
            "entrypoints": {
                key: "placeholder" for key in
                ("human", "agent", "protocol", "contributing", "schema", "example")
            },
        }
        example = {"authority_effect": "none"}
        with patch.object(validator, "load_json", side_effect=[beacon, {}, example]), \
             patch.object(validator, "require_file"), \
             patch.object(Path, "read_text", return_value=" ".join(validator.REQUIRED_INVARIANTS)):
            return validator.main()

    def test_exact_capability_set_passes(self):
        self.assertEqual(self.check_states(sorted(validator.EXPECTED_CAPABILITY_STATES)), 0)

    def test_duplicate_capability_state_fails(self):
        states = sorted(validator.EXPECTED_CAPABILITY_STATES) + ["proven"]
        with self.assertRaisesRegex(AssertionError, "capability state drift"):
            self.check_states(states)


if __name__ == "__main__":
    unittest.main()
