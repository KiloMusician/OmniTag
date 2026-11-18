import unittest
from evidence import Claim, EvidenceLedger, verify_capsule

class EvidenceTests(unittest.TestCase):
    def test_capsule_round_trip(self):
        ledger = EvidenceLedger("s1")
        ledger.add(Claim("repo", "status", "review", "PR-33", "observed", "proven"))
        self.assertTrue(verify_capsule(ledger.capsule()))

    def test_tampering(self):
        ledger = EvidenceLedger("s1")
        ledger.add(Claim("repo", "status", "review", "PR-33"))
        capsule = ledger.capsule()
        capsule["claims"][0]["value"] = "merged"
        self.assertFalse(verify_capsule(capsule))

    def test_conflict_preservation(self):
        ledger = EvidenceLedger("s1")
        ledger.add(Claim("repo", "state", "open", "source-a"))
        ledger.add(Claim("repo", "state", "closed", "source-b"))
        self.assertEqual(len(ledger.conflicts()), 1)
        self.assertEqual(len(ledger.conflicts()[0]["alternatives"]), 2)

    def test_deduplication(self):
        ledger = EvidenceLedger("s1")
        claim = Claim("repo", "state", "open", "source-a")
        self.assertEqual(ledger.add(claim), ledger.add(claim))
        self.assertEqual(len(ledger.claims), 1)

    def test_invalid_classification(self):
        with self.assertRaises(ValueError):
            Claim("repo", "state", "open", "source", capability="superuser")

    def test_rejects_forged_conflicts(self):
        ledger = EvidenceLedger("s1")
        capsule = ledger.capsule()
        capsule["conflicts"].append({"subject": "fake"})
        self.assertFalse(verify_capsule(capsule))

if __name__ == "__main__":
    unittest.main()
