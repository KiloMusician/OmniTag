# Historical local LLM onboarding: recovered lessons

[Msg⛛{LOCAL-LLM-ONBOARDING-20261022}] [Ctx⛛{HistoricalRecovery}] [State⛛{Proposed}] [Role⛛{Documentation}]

## Provenance and scope

Recovered from a historical ChatGPT conversation about helping a friend install a local companion/coding/Linux assistant on Windows 10. The conversation included Windows 10 build 19045.5965, an AMD Phenom II X4 965, 16 GB system RAM, an **unidentified** 8 GB graphics card, and about 200 GB free storage. These are **historical user reports**, not current hardware probes. The conversation reported WSL, Python, VS Code/Copilot and GitHub Desktop installed, but provided no command output confirming versions or GPU compatibility.

No current local machine, build, or benchmark was inspected for this recovery.

## Lessons to retain

1. **Detect, then recommend.** Obtain GPU vendor/model, driver, compute support, CPU instruction-set support, OS build, virtualization status, RAM, disk, and target runtime before suggesting models or acceleration.
2. **Do not infer CUDA from VRAM.** An 8 GB card may be NVIDIA, AMD, Intel, or unsupported. GPU memory is not a CUDA capability check.
3. **Check older CPU/WSL compatibility.** WSL 2 depends on virtualization and hardware support; legacy Phenom II systems require explicit validation. Do not assume a successful `wsl --install` proves WSL 2 is running.
4. **Distinguish runtime choices.** llama.cpp/GGUF or Ollama-style workflows do not universally require Python, PyTorch, Transformers, Git LFS, CUDA Toolkit, or Docker. Select dependencies after choosing runtime.
5. **Verify model identities.** Mistral Small 3.2 is a roughly 24B-parameter model, not 3.2B. The cited 'GPT-NeoX 2.7B' identity was not verified. Never invent Hugging Face repository IDs. DeepSeek models remain on Hugging Face; assess exact variant, quantization, and hardware fit.
6. **Separate install state from assumption.** Maintain `unknown / requested / running / verified / failed` statuses with command evidence and timestamps. Do not say Ubuntu or Python is configured merely because installation was started.
7. **Keep shells and environments distinct.** Windows PowerShell, CMD, Git Bash, and Bash inside a WSL Linux distribution are different. A Windows Python install does not imply Linux Python is installed. Installing Ubuntu typically supplies Bash; WSL itself is the compatibility layer.
8. **GitHub access boundaries.** GitHub Desktop, Copilot, ChatGPT's GitHub connector, and an OpenAI API client are distinct. Do not require users to paste personal access tokens into source code. Use minimum privileges and credential storage.
9. **Respect the user's one-step-at-a-time request.** Give a single diagnostic/action and wait for output rather than repeating whole installation plans.
10. **Model selection is a measurement task.** Compare small current instruction-tuned GGUF models using memory fit, token speed, coding/Linux assistance quality, conversation quality, and CPU fallback. Quantization, KV cache, and context length matter.

## Proposed validation gates

- Hardware inventory and virtualization/WSL capability report.
- Runtime decision record: Windows-native vs WSL, CPU vs GPU, llama.cpp vs Python framework.
- Download plan with verified publisher/model IDs, licenses, quantization, file sizes, and checksums where available.
- Short reproducible smoke test, measured memory and tokens/sec, basic Linux/coding prompt set.
- Dependency state ledger with exact commands, exit codes, and rollback instructions.
- No unattended privilege escalation, unreviewed downloads, or credential collection.

## Suggested OmniTag receipt

```text
[Msg⛛{LOCAL-LLM-SETUP}]
[Ctx⛛{EnvironmentProbe}]
[State⛛{Unknown}]
[Ref⛛{hardware-inventory}]
[Act⛛{VerifyBeforeInstall}]
```

## Boundary

This is a **historical documentation artifact**, not proof of current runtime compatibility, installation success, or model performance. It proposes checks rather than performing them. No repository code or machine configuration is changed by this note.
