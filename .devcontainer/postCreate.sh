#!/bin/bash
set -e

# Codex CLI（apply_patch を含む）
npm install -g @openai/codex

# npm グローバルバイナリ（apply_patch 等）を PATH に追加
NPM_BIN=$(npm config get prefix)/bin
echo "export PATH=\"${NPM_BIN}:\$PATH\"" >> ~/.bashrc
echo "export PATH=\"${NPM_BIN}:\$PATH\"" >> ~/.zshrc
export PATH="${NPM_BIN}:$PATH"

# uv
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# バージョン確認
codex --version || true
apply_patch --help > /dev/null 2>&1 && echo "apply_patch: OK" || echo "apply_patch: not found"
gh --version || true
uv --version || true

# --- 以下はプロジェクトの技術スタックに応じて追加 ---

# Python 開発ツールの場合:
# uv tool install ruff
# uv tool install basedpyright

# AWS CDK の場合:
# npm install -g aws-cdk
# cdk --version || true
