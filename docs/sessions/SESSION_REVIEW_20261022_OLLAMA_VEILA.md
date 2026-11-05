# Session harvest: macOS Ollama and Veila (2026-10-22)

[Msg⛛{20261022-OLLAMA-VEILA}] [State⛛{Prototype}] [Ref⛛{issue-42}]

## Provenance
Historical session supplied by operator. Current public OmniTag README and recent PRs reviewed through GitHub. Direct git clone/fetch in local container failed due DNS; no local repository build or CI validation is claimed. Existing #38 covers general local-LLM lessons. This contribution focuses macOS setup.

## Novel Ideas & Investigations

### P1: Single-server ownership
Earlier proposed installer installed both Homebrew formula and cask, then started a brew service. Choose one manager, probe /api/version before starting anything, and do not spawn a second server.

### P1: Credential and config preservation
Avoid exporting OPENAI_API_KEY into global shell profile; preserve existing ~/.continue/config.yaml. Continue YAML with provider: ollama is distinct from Claude Code's Anthropic-compatible transport.

### P2: Veila trace provenance challenge
Veila said it had synchronized traces and self-learning. A language-model acknowledgment is not proof of persistent memory, trace API, or integration. Test cross-session recall with exact IDs and independently inspectable receipts.

### P2: Symbolic interoperability benchmark
Use OmniTag, MegaTag, PhoenixTag, Rosetta, ConLang, Context Texture and Unicode planes 0-16 as test corpora for parsing, grapheme handling, and source-attributed handoffs. Symbols are not authorization or evidence of implementation.

## Validation and next steps
- Bash syntax check completed on local prototype; macOS runtime not available.
- Test Apple Silicon and Intel, idempotent repeated runs, service ownership, offline inference, model availability, Continue config compatibility.
- Claude Code integration must be separately verified with an Anthropic-compatible adapter and tool-calling support.
- GitHub issue #42 tracks acceptance and follow-up.
