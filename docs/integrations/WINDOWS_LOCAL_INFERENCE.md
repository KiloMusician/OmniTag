# Windows local inference integration investigation

[Msg⛛{LOCAL-INFERENCE-20261023}] [Ctx⛛{Tooling}] [State⛛{Proposed}]

## Session harvest

A Windows development session compared Ollama alternatives: LM Studio, Jan, GPT4All, llama.cpp, and KoboldCpp. The actionable opportunity is to connect local inference runtimes to VS Code extensions and CLI agents without coupling a coding workflow to one model server.

## Proposed architecture

Runtime -> explicit API adapter -> VS Code or CLI consumer.

An adapter should record endpoint, protocol, model identifier, timeout, streaming behavior and independently tested capabilities. OpenAI-compatible HTTP alone does not prove tool calling, embeddings, fill-in-middle or structured output.

## Read-only Windows smoke test

With LM Studio server enabled and a model loaded, run:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:1234/v1/models' -Method Get
```

This tests model-listing reachability only, not successful generation. Use the returned model ID for a subsequent read-only chat request. Keep the service bound to loopback unless intentionally configured otherwise.

## Novel investigations

1. P1 Tooling: design a backend capability probe and normalized feature manifest; validate model discovery, chat, streaming, and errors independently.
2. P2 Architecture: compare actual requests from a VS Code client and a CLI client against Ollama and LM Studio before building an adapter.
3. P2 Performance: benchmark cold start, generation speed, RAM/VRAM usage, and concurrency on Windows. Never substitute estimates for measurements.
4. P2 Reliability: define fallback behavior for unreachable runtimes, unsupported features, and timeouts.

## Verification boundary and handoff

Repository documentation inspected: README.md, AGENTS.md, CONTRIBUTING.md, docs/PROTOCOL.md, and omnitag.agent-beacon.json. No local Windows runtime, build, test suite, or actual VS Code/CLI integration was exercised in this session. The next agent should run one backend with one VS Code consumer and one CLI consumer, record exact commands and observed results, then propose implementation in the appropriate code repository.

[State⛛{Proposed}] [Act⛛{Verify}]
