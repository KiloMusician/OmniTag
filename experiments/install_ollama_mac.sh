#!/usr/bin/env bash
set -euo pipefail
API=http://127.0.0.1:11434
command -v brew >/dev/null || { echo 'Install Homebrew first: https://brew.sh'; exit 1; }
if ! command -v ollama >/dev/null; then brew install ollama; fi
if curl -fsS "$API/api/version" >/dev/null 2>&1; then
  echo 'Ollama already running; preserving current server owner.'
else
  brew services start ollama
  for i in {1..30}; do
    curl -fsS "$API/api/version" >/dev/null 2>&1 && break
    sleep 1
  done
fi
curl -fsS "$API/api/version" >/dev/null || { echo 'Ollama API unavailable'; exit 1; }
for model in qwen2.5-coder:3b llama3.2:3b qwen2.5-coder:7b; do
  if ollama list | awk 'NR>1 {print $1}' | grep -Fxq "$model"; then
    echo "Already installed: $model"
  else
    ollama pull "$model"
  fi
done
mkdir -p "$HOME/.continue"
if [[ ! -e "$HOME/.continue/config.yaml" ]]; then
cat > "$HOME/.continue/config.yaml" <<'YAML'
name: Local Ollama Starter
version: 1.0.0
schema: v1
models:
  - name: Qwen Coder 3B
    provider: ollama
    model: qwen2.5-coder:3b
    roles: [chat, edit, apply]
  - name: Qwen Coder 7B
    provider: ollama
    model: qwen2.5-coder:7b
    roles: [chat, edit, apply]
  - name: Llama 3.2 3B
    provider: ollama
    model: llama3.2:3b
    roles: [chat]
YAML
else
  echo 'Preserving existing Continue configuration.'
fi
ollama list
echo 'Ready. Claude Code requires separate Anthropic-compatible configuration.'
