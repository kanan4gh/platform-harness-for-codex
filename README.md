# Coord Prompt Studio

Coord Prompt Studio は、コーディネート画像から画像生成向けの服装再現プロンプトを抽出し、ChatGPT Web UIで得た抽出結果と比較評価するローカルCLIツールです。

MVP 0では画像生成APIを呼び出しません。コーデ抽出、ChatGPT結果の貼り付け保存、比較評価の記録、セッション参照に集中します。

## セットアップ

```bash
uv python install 3.12
uv venv .venv
uv sync
```

## CLI

ヘルプを表示します。

```bash
uv run python -m coord_prompt_studio.cli --help
```

コーディネート画像から抽出セッションを作成します。

```bash
uv run python -m coord_prompt_studio.cli extract ./path/to/outfit.png --input-type photo --note "検証用"
```

イラスト画像の場合は `--input-type illustration` を指定します。

```bash
uv run python -m coord_prompt_studio.cli extract ./path/to/outfit.png --input-type illustration
```

ChatGPT Web UIで得た抽出結果を保存済みセッションへ追加します。

```bash
uv run python -m coord_prompt_studio.cli add-chatgpt 20260612-083000 --file ./chatgpt-result.txt
```

比較評価を記録します。

```bash
uv run python -m coord_prompt_studio.cli evaluate 20260612-083000 \
  --coverage 同等 \
  --colors-patterns 不足 \
  --materials 要改善 \
  --silhouette 同等 \
  --prompt-usability 同等 \
  --note "素材感の表現が少し弱い"
```

保存済みセッションを確認します。

```bash
uv run python -m coord_prompt_studio.cli list
uv run python -m coord_prompt_studio.cli show 20260612-083000
```

## 開発コマンド

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
```

---

# Codex ハーネステンプレート

OpenAI Codex CLI 向けのスペック駆動開発（SDD）ハーネスです。このテンプレートを複製することで、Codex エージェントがプロジェクトの方針・技術スタック・構造を理解した状態で開発を支援できる環境を即座に構築できます。

## このテンプレートについて

### ハーネスとは

「エンジンを動かすために必要な、エンジン以外のすべて」。Codex CLI（LLM エンジン）を有効に動かすための文脈注入・プロセス定義の仕組みを指します。

### 構成

```
AGENTS.md              # Codex CLI へのコンテキスト注入（このファイルを編集してプロジェクト情報を記入）
.devcontainer/         # 開発環境定義（Codex CLI インストール済み）
.steering/
└── _template/         # 機能実装時にコピーして使うスペックテンプレート
    ├── requirements.md
    ├── design.md
    └── tasklist.md
docs/                  # プロジェクト永続ドキュメント（テンプレート）
    ├── product-requirements.md
    ├── functional-design.md
    ├── architecture.md
    ├── repository-structure.md
    ├── development-guidelines.md
    └── glossary.md
```

## はじめに

セットアップから動作確認・SDD ワンサイクルまでを順番に体験できる **[オンボーディングガイド](ONBOARDING.md)** を用意しています。初めて使う方はこちらから始めてください。

## クイックスタート

### 1. テンプレートを複製する

GitHub の **"Use this template"** ボタンをクリックして、新しいリポジトリを作成します。

### 2. devcontainer で開く（推奨）

VS Code で複製したリポジトリを開き、「Reopen in Container」を選択します。Codex CLI がインストール済みの環境が自動で構築されます。

> devcontainer を使わない場合は、`npm install -g @openai/codex` で Codex CLI をローカルにインストールしてください。

### 3. プロジェクト情報を記入する

`AGENTS.md` を開き、以下のセクションをプロジェクト情報で書き換えます：

- **プロダクト定義**: プロダクト名・ビジョン・目的
- **技術スタック**: 言語・フレームワーク・セットアップ手順
- **リポジトリ構造**: ディレクトリ構造・主要ファイルの役割

または、チャットで以下を入力して対話的にセットアップします：

```
setup-project を実行してください
```

Codex が対話形式でプロダクト情報をヒアリングし、`docs/` の6ファイルと `AGENTS.md` を更新します。

### 4. 最初の機能を実装する

セットアップが完了したら、チャットで以下を入力します：

```
add-feature を実行してください
```

Codex が SDD フロー（requirements → design → tasklist → 実装 → PR）をガイドします。

## できること・できないこと

| 機能 | 対応状況 | 備考 |
|-----|---------|------|
| 文脈注入（プロセス・プロダクト・技術・構造） | ✅ | `AGENTS.md` の5セクション構造 |
| SDD フロー（スペック作成 → 実装 → PR） | ✅ | `AGENTS.md` のワークフローセクションで定義 |
| devcontainer による環境再現 | ✅ | `.devcontainer/` に Codex CLI インストール済み |
| フック（ファイル保存時の自動実行等） | ❌ | Codex CLI にネイティブ機能なし |
| カスタムエージェント定義 | ❌ | Codex CLI にネイティブ機能なし |
| 粒度別コンテキスト注入（always/auto/manual） | ❌ | Codex CLI は全内容を常時読み込み |

## Claude Code ハーネスから移行する場合

Claude Code（CLAUDE.md）でスペック駆動開発をしていた方向けの対応表です。

| Claude Code 要素 | Codex CLI での対応先 |
|----------------|---------------------|
| `CLAUDE.md` 汎用層（開発プロセス原則） | `AGENTS.md`「開発プロセス原則」セクション（編集不要） |
| `CLAUDE.md` プロダクト固有層 | `AGENTS.md`「プロダクト定義」セクション |
| `CLAUDE.md` 技術スタック固有層 | `AGENTS.md`「技術スタック」セクション |
| `.steering/YYYYMMDD-xxx/` 作業スペック | `.steering/YYYYMMDD-xxx/`（構造は同一） |
| `settings.json` hooks | `AGENTS.md`「ワークフロー」セクション（手動トリガー） |
| `.mcp.json` | `~/.codex/config.toml`（Codex グローバル設定） |
| `CLAUDE.md` に記載していたリポジトリ構造 | `AGENTS.md`「リポジトリ構造」セクション |

## MCP サーバーの設定

Codex CLI の MCP サーバーはユーザーグローバル設定（`~/.codex/config.toml`）で管理します。リポジトリには含めません。

```toml
# ~/.codex/config.toml の例
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
```

## ライセンス

MIT
