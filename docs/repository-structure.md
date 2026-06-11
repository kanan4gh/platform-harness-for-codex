# リポジトリ構造定義書 (Repository Structure Document)

## ディレクトリ構造

MVP 0〜2は、Codex CLIまたはCodex SDKを使うPython製ローカルツールとして構成する。開発環境はdevcontainerを使わず、ローカルのPython `.venv`で動かし、依存管理には `uv` を使う。最終画像生成はChatGPT Web UIへ持ち出すため、アプリ内の画像生成API連携は初期構造に含めない。

```
platform-harness-for-codex/
├── AGENTS.md
├── README.md
├── ONBOARDING.md
├── .steering/
│   ├── _template/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasklist.md
│   └── YYYYMMDD-xxx/
├── docs/
│   ├── product-requirements.md
│   ├── functional-design.md
│   ├── architecture.md
│   ├── repository-structure.md
│   ├── development-guidelines.md
│   └── glossary.md
├── prompts/
│   ├── coordinate_extraction.md
│   ├── person_identity_improvement.md
│   ├── negative_prompt_improvement.md
│   └── final_prompt_template.md
├── src/
│   └── coord_prompt_studio/
│       ├── __init__.py
│       ├── cli.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── feedback.py
│       │   ├── prompt_composition.py
│       │   ├── prompt_parts.py
│       │   ├── trials.py
│       │   └── variation.py
│       ├── use_cases/
│       │   ├── __init__.py
│       │   ├── compose_final_prompt.py
│       │   ├── create_variation_prompt.py
│       │   ├── extract_coordinate_prompt.py
│       │   ├── record_chatgpt_comparison.py
│       │   └── record_review.py
│       ├── adapters/
│       │   ├── __init__.py
│       │   ├── codex.py
│       │   └── image_storage.py
│       └── repositories/
│           ├── __init__.py
│           ├── feedback.py
│           ├── image_assets.py
│           ├── prompt_parts.py
│           └── trials.py
├── data/
│   ├── images/
│   ├── prompt_parts/
│   ├── sessions/
│   └── feedback/
├── templates/
│   └── layouts/
├── tests/
│   ├── domain/
│   ├── use_cases/
│   └── adapters/
├── .venv/
├── .python-version
├── pyproject.toml
└── uv.lock
```

## 主要ディレクトリ・ファイルの役割

| パス | 役割 |
|-----|------|
| `AGENTS.md` | Codex CLIへの常時コンテキスト注入。開発プロセス、プロダクト定義、技術スタック、構造を含む |
| `.steering/` | 作業単位のスペックファイル群。意思決定の履歴としてGit管理する |
| `.steering/_template/` | スペック作成時のテンプレート。直接編集せず、コピーして使う |
| `docs/` | プロジェクト全体の永続ドキュメント。PRD、機能設計、アーキテクチャ、構造、ガイドライン、用語を定義する |
| `prompts/` | Codexへ渡すプロンプトテンプレート、ChatGPT Web UI貼り付け用テンプレートを管理する |
| `src/coord_prompt_studio/` | Pythonローカルツール本体 |
| `src/coord_prompt_studio/cli.py` | CLIエントリポイント |
| `src/coord_prompt_studio/domain/` | プロンプト部品、評価、試行履歴、合成ルールなどのドメインモデル |
| `src/coord_prompt_studio/use_cases/` | CLIから呼ばれるアプリケーション操作 |
| `src/coord_prompt_studio/adapters/` | Codex CLI/SDK、画像保存など外部境界の実装 |
| `src/coord_prompt_studio/repositories/` | JSON/YAML/SQLiteなど永続化境界の実装 |
| `data/` | ローカル実行時の画像、抽出結果、プロンプト部品、評価履歴の保存先。必要に応じてGit管理対象外にする |
| `templates/layouts/` | Post-MVPの雑誌風コラージュ、コーデ説明画像用のレイアウトテンプレート |
| `tests/` | pytestによるテストコード |
| `.venv/` | ローカルPython仮想環境。Git管理しない |
| `.python-version` | Pythonバージョン固定 |
| `pyproject.toml` | Pythonプロジェクト設定、依存関係、ツール設定 |
| `uv.lock` | uvによる依存関係ロックファイル |

## ファイル配置の判断基準

新しいファイルを作成する際の配置先:

| 内容 | 配置先 |
|-----|-------|
| Codex CLIに常時参照させたい情報 | `AGENTS.md` の該当セクションを更新 |
| 今回の作業に特化したスペック | `.steering/YYYYMMDD-[機能名]/` に配置 |
| プロジェクト全体の永続的な定義 | `docs/` に配置 |
| アイデア・ブレインストーミングメモ | `docs/ideas/` に配置 |
| Codexへ渡す作業プロンプト | `prompts/` に配置 |
| ChatGPT Web UIへ貼り付けるテンプレート | `prompts/` に配置 |
| ドメインモデル・純粋ロジック | `src/coord_prompt_studio/domain/` に配置 |
| ユースケース | `src/coord_prompt_studio/use_cases/` に配置 |
| 外部境界・Codex連携 | `src/coord_prompt_studio/adapters/` に配置 |
| 永続化 | `src/coord_prompt_studio/repositories/` に配置 |
| ローカル実行データ | `data/` に配置 |
| テストコード | `tests/` 配下に配置 |
| レイアウトテンプレート | `templates/layouts/` に配置 |

## 命名規則

### ファイル名

- Pythonソースファイル: `snake_case.py`
- Pythonテストファイル: `test_[対象モジュール名].py`
- Markdownドキュメント: `kebab-case.md`
- Codex/ChatGPT向けプロンプトテンプレート: `snake_case.md`
- レイアウトテンプレート: `kebab-case.json` または `kebab-case.yaml`
- ローカルデータファイル: `YYYYMMDD-HHMMSS-[内容].json`

### ディレクトリ名

- Pythonパッケージ配下: `snake_case`
- ドキュメント、テンプレート、作業スペック: 小文字・ハイフン区切り
- `.steering/` の作業ディレクトリ: `YYYYMMDD-[タスク名]`

### ブランチ名

- 機能追加: `feat/[機能名]`
- バグ修正: `fix/[修正内容]`
- ドキュメント: `docs/[内容]`
- 初期セットアップ: `setup/[内容]`

## Git管理方針

- `docs/`, `prompts/`, `src/`, `tests/`, `templates/` はGit管理する
- `.steering/` は意思決定履歴としてGit管理する
- `data/` は原則としてローカル実行データを置くため、実装時に`.gitignore`対象を検討する
- `.venv/` はGit管理しない
- 実在人物や第三者画像、生成済み画像、個人のプロンプト履歴は不用意にコミットしない
