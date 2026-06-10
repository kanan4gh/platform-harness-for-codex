#!/bin/bash
set -e

# Codex CLI
npm install -g @openai/codex

# バージョン確認
codex --version || true
gh --version || true

# --- 以下はプロジェクトの技術スタックに応じて追加 ---

# Python (uv) の場合:
# curl -LsSf https://astral.sh/uv/install.sh | sh
# echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
# export PATH="$HOME/.local/bin:$PATH"
# uv tool install ruff
# uv tool install basedpyright

# Node.js プロジェクトの場合:
# npm install

# AWS CDK の場合:
# npm install -g aws-cdk
# cdk --version || true
