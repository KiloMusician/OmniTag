"""
omnitag_tests.py — round-trip and parser conformance suite.

Each case is a dict. Fields:
  id, name, input, expect_parse (bool),
  expect_roundtrip_equal (bool, only if parse succeeds),
  expect_output (optional canonical form when != input),
  expect_warning (optional warning code),
  expect_error_code (when expect_parse is False).
"""
from __future__ import annotations
import unicodedata
from omnitag import parse, serialize, ParseError, canonicalize

CASES = [
    dict(id="RT-001", name="minimal tag",
         input="[Msg⛛{X}]",
         expect_parse=True, expect_roundtrip_equal=True),

    dict(id="RT-002", name="canonical preamble",
         input="[Msg⛛{SC-ASCENSION-20261008-01}][Date⛛{2026-10-08}][Ctx⛛{SC-GSV-INTEGRATION}]",
         expect_parse=True, expect_roundtrip_equal=True),

    dict(id="RT-003", name="full example sequence",
         input=("[Msg⛛{X}]▲[Data]⦿⦾Media⦾⦿⟹{Algo}⟸↺[FB]Ω⊗{QM}"
                "↠t[⏳]↞⚙{Dyn}⚙🌐{Ctx}🌐🔁{🔄}🔁⛓[⚙️]⛓⚡{⚙️}⚡⭐{⭐}⭐✨{✨}✨"),
         expect_parse=True, expect_roundtrip_equal=True),

    dict(id="RT-004", name="emoji with variation selector preserved",
         input="[Task⛛{\u2699\uFE0F}]",
         expect_parse=True, expect_roundtrip_equal=True,
         must_contain="\u2699\uFE0F"),

    dict(id="RT-005", name="NFD input normalizes to NFC on output",
         input="[Ctx⛛{caf\u0065\u0301}]",       # café in NFD
         expect_parse=True, expect_roundtrip_equal=False,
         expect_output="[Ctx⛛{caf\u00e9}]",      # café in NFC
         expect_warning="NON_CANONICAL_NFC"),

    dict(id="RT-006", name="combining mark preserved",
         input="[Ref⛛{a\u0332b}]",               # a + combining low line + b
         expect_parse=True, expect_roundtrip_equal=True),

    dict(id="RT-007", name="RTL content preserved",
         input="[Ctx⛛{\u0645\u0631\u062d\u0628\u0627}]",   # مرحبا
         expect_parse=True, expect_roundtrip_equal=True),

    dict(id="RT-008", name="literal bypasses tag parsing",
         input="❰[not a tag⛛{still not}]❱",
         expect_parse=True, expect_roundtrip_equal=True,
         expect_no_tag=True),

    dict(id="RT-009", name="nested sequence",
         input="⟦[A⛛{1}]↔[B⛛{2}]⟧",
         expect_parse=True, expect_roundtrip_equal=True),

    dict(id="RT-010", name="unknown connector preserved + warned",
         input="[A⛛{1}]\U0001F702[B⛛{2}]",      # 🜂 alchemical fire
         expect_parse=True, expect_roundtrip_equal=True),

    dict(id="RT-011", name="unbalanced braces — fail cleanly",
         input="[Msg⛛{unclosed]",
         expect_parse=False, expect_error_code="UNTERMINATED_TAG_BODY"),

    dict(id="RT-012", name="empty body allowed",
         input="[State⛛{}]",
         expect_parse=True, expect_roundtrip_equal=True),

    dict(id="RT-013", name="whitespace inside body preserved verbatim",
         input="[Ctx⛛{  two  spaces  }]",
         expect_parse=True, expect_roundtrip_equal=True),

    dict(id="RT-014", name="NFKC would fold but we do not",
         input="[Ctx⛛{\u2460\u2461\u2462}]",    # ①②③
         expect_parse=True, expect_roundtrip_equal=True,
         must_contain="\u2460\u2461\u2462"),

    dict(id="RT-015", name="ZWJ family emoji preserved",
         input="[Ctx⛛{\U0001F468\u200D\U0001F469\u200D\U0001F467}]",
         expect_parse=True, expect_roundtrip_equal=True,
         must_contain="\u200D"),
    dict(id="RT-016", name="Nested tags inside payload preserved",
         input="[Nest⛛{Outer:[State⛛{Observed}]}]",
         expect_parse=True, expect_roundtrip_equal=True),
    dict(id="RT-017", name="NFD plain text outside tags normalizes",
         input="caf\u0065\u0301 [Msg⛛{7}]",
         expect_parse=True, expect_roundtrip_equal=False,
         expect_output="café [Msg⛛{7}]", expect_warning="NON_CANONICAL_NFC"),
    dict(id="RT-018", name="OmniTag extensions remain raw, not executable",
         input="[Role⛛{ADMIN}] ⟹{not-authority} ⚡{⚙️}",
         expect_parse=True, expect_roundtrip_equal=True),
]

# ─── runner ───────────────────────────────────────────────────────────────

def _has_tag(node) -> bool:
    from omnitag import Tag, Nested
    if isinstance(node, Tag):
        return True
    if isinstance(node, Nested):
        return any(_has_tag(x) for x in node.sequence)
    return False

def run() -> int:
    passed, failed = 0, 0
    print(f"{'ID':<8} {'RESULT':<6} NAME")
    print("─" * 72)
    for c in CASES:
        try:
            doc = parse(c["input"])
        except ParseError as e:
            if not c["expect_parse"] and e.code == c.get("expect_error_code"):
                print(f"{c['id']:<8} {'PASS':<6} {c['name']}  (rejected: {e.code})")
                passed += 1
            else:
                print(f"{c['id']:<8} {'FAIL':<6} {c['name']}  (unexpected error: {e.code})")
                failed += 1
            continue

        if not c["expect_parse"]:
            print(f"{c['id']:<8} {'FAIL':<6} {c['name']}  (expected error, got success)")
            failed += 1
            continue

        out = serialize(doc)
        problems = []

        if c.get("expect_roundtrip_equal") and out != c["input"]:
            problems.append(f"round-trip mismatch: {out!r} != {c['input']!r}")
        if "expect_output" in c and out != c["expect_output"]:
            problems.append(f"canonical mismatch: {out!r} != {c['expect_output']!r}")
        if "expect_warning" in c:
            codes = {w.code for w in doc.warnings}
            if c["expect_warning"] not in codes:
                problems.append(f"missing warning {c['expect_warning']}")
        if "must_contain" in c and c["must_contain"] not in out:
            problems.append(f"missing sequence {c['must_contain']!r}")
        if c.get("expect_no_tag"):
            if any(_has_tag(e) for e in doc.elements):
                problems.append("found Tag node inside literal")

        if problems:
            print(f"{c['id']:<8} {'FAIL':<6} {c['name']}")
            for p in problems:
                print(f"         └─ {p}")
            failed += 1
        else:
            print(f"{c['id']:<8} {'PASS':<6} {c['name']}")
            passed += 1

    print("─" * 72)
    print(f"passed: {passed}   failed: {failed}   total: {len(CASES)}")

    # ── meta-test: two separate relevant mutations, not a false assumption
    # RT-004 contains VS16 but no ZWJ; RT-015 contains ZWJ but no VS16.
    print("\nMeta-test: independently strip VS16 and ZWJ; each relevant case must fail.")
    import omnitag
    original = omnitag._ser
    mutation_tests = (("RT-004", "\uFE0F"), ("RT-015", "\u200D"))
    try:
        for case_id, removed in mutation_tests:
            def broken(el):
                return original(el).replace(removed, "")
            omnitag._ser = broken
            case = next(c for c in CASES if c["id"] == case_id)
            mutated = serialize(parse(case["input"]))
            if mutated == case["input"]:
                print(f"meta-test FAIL: {case_id} did not detect {removed!r} mutation")
                failed += 1
            else:
                print(f"meta-test PASS: {case_id} detects forbidden deletion")
    finally:
        omnitag._ser = original

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    import sys
    # Preserve Unicode input fixtures while making console diagnostics safe on
    # Windows terminals whose output encoding cannot represent OmniTag glyphs.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    sys.exit(run())
