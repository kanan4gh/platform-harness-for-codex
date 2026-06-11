# Coord Prompt Studio - 開発ガイド

<!-- このファイルは Codex CLI がプロジェクト文脈を理解するための設定ファイルです。
     セクション1（開発プロセス原則）はハーネス共通のルールです。編集しないでください。
     セクション2〜4（プロダクト定義・技術スタック・リポジトリ構造）をプロジェクト情報で書き換えてください。
     セクション5（ワークフロー）はハーネス共通のルールです。編集しないでください。 -->

---

## 開発プロセス原則

### スペック駆動開発（SDD）フロー

全ての機能開発・バグ修正は以下のフローで行う:

```
1. ドキュメント確認  : docs/ の永続ドキュメントで方針を確認
2. Issue 作成       : GitHub Issue を作成（`gh issue create` コマンド）
3. スペック作成     : .steering/_template/ をコピーして YYYYMMDD-xxx/ を作成
4. 要求定義         : requirements.md を記入（Issue URL を必ず記載）
5. 設計             : design.md を記入
6. タスク計画       : tasklist.md を記入
7. 実装             : tasklist.md のタスクを順番に実行・チェック
8. PR 作成・マージ  : フィーチャーブランチ → PR → main へマージ
9. リリース         : 必要に応じて GitHub Release を作成
```

### 作業スペックの使い方

**ディレクトリ命名規則**:

```
.steering/
├── _template/               # テンプレート（直接編集しない）
├── 20250115-add-login/      # 機能実装単位（_template/ をコピーして作成）
│   ├── requirements.md      # 要求仕様（関連 Issue URL を必須記入）
│   ├── design.md            # 実装設計
│   └── tasklist.md          # タスクリスト（進捗を随時チェック）
└── 20250120-fix-auth-bug/
    └── ...
```

命名規則: `YYYYMMDD-[タスク名（英小文字・ハイフン区切り）]`

**スペック作成手順**:

1. GitHub Issue を作成する（`gh issue create`）
2. `.steering/_template/` をコピーして `YYYYMMDD-[タスク名]/` として配置する
3. `requirements.md` を記入し、**ユーザーの確認を得てから** `design.md` に進む
4. `design.md` を記入し、**ユーザーの確認を得てから** `tasklist.md` に進む
5. `tasklist.md` を記入し、**ユーザーの確認を得てから**実装を開始する

> **重要**: 各ドキュメントは1ファイルずつ作成する。ユーザーが確認・承認するまで次のステップに進まない。

### tasklist.md の管理ルール

- タスク開始時に `[ ]` → `[x]` へ更新する
- **全タスクが `[x]` になるまで実装を継続する**
- 「時間の都合により後回し」は禁止
- 技術的理由でスキップする場合は理由を明記する

### ドキュメント管理

**永続ドキュメント（`docs/`）**:
- プロジェクト全体の「何を作るか」「どう作るか」を定義する
- 頻繁に更新しない（変更は方針転換のシグナル）
- 実装後に設計と実態が乖離していれば更新する

**作業スペック（`.steering/`）**:
- 特定の作業に特化したドキュメント
- 作業ごとに新規作成し、履歴として保持する（`.gitignore` に含めない）

### PR・リリースフロー

**PR 作成**:
- `main` へ直接コミットしない（機能実装コードも含む）
- フィーチャーブランチ → PR → マージ の手順を踏む

**リリース**:
- PR マージ後、必要に応じて `gh release create` で GitHub Release を作成する
- リリース前に関連 Issue をクローズする（`gh issue close <番号>`）

---

## プロダクト定義

### プロダクト名

Coord Prompt Studio - コーデ画像から画像生成プロンプトを組み立てるローカルツール

### ビジョン

画像生成における「服装の再現」「人物設定の固定」「不要要素の抑制」を、プロンプト部品の組み合わせとして扱えるようにする。MVP 0〜2ではCodex CLIまたはCodex SDKを使ったローカルツールとして実装し、最終画像生成のみChatGPT Web UIへ持ち出す。

### 目的

- 実写画像、アニメ風イラスト画像、既存のコーデ再現プロンプトからコーデ抽出プロンプトを作成する
- 人物固定、コーデ抽出、背景、撮影、ポーズ、ネガティブ抑制の各プロンプト部品を管理する
- プロンプト部品を合成し、ChatGPT Web UIへ貼り付けやすい最終プロンプトを作成する
- MVP 0では、コーデ画像からChatGPT同等のコーデ抽出結果が得られるかを検証する
- 生成結果の良かった/悪かった、失敗再生成、派生生成を記録し、次回のプロンプト改善につなげる
- 初期MVPでは画像生成APIを直接呼び出さず、APIコストを抑えて抽出・合成・評価のワークフローを検証する

### ターゲットユーザー

画像生成を使ってキャラクター画像、ファッション画像、SNS向けビジュアル、創作素材を作る個人クリエイター。複数パターンの衣装案やスタイリング案を効率よく試したいデザイナー、企画者、プロンプト作成者も対象とする。

### 参照ドキュメント

> このセクションは `docs/` 配下のドキュメント一覧です。詳細はそれぞれのファイルを参照してください。

- `docs/product-requirements.md` — プロダクト要求定義書（PRD）
- `docs/functional-design.md` — 機能設計書・設計指針
- `docs/architecture.md` — 技術仕様書・アーキテクチャ設計
- `docs/repository-structure.md` — リポジトリ構造定義書
- `docs/development-guidelines.md` — 開発ガイドライン・コーディング規約
- `docs/glossary.md` — ユビキタス言語定義（用語集）

---

## 技術スタック

### 使用技術

- 実行基盤: Codex CLI / Codex SDK
- 言語: Python 3.12+
- 仮想環境: `.venv`
- 依存管理: uv + `pyproject.toml` + `uv.lock`
- CLI: Typer または argparse
- Codex連携: `codex` CLI subprocess / `openai-codex` Python SDK
- データストア: JSON/YAML files、必要に応じてSQLite
- テスト: pytest
- リンター/整形: ruff
- 型チェック: basedpyright または pyright

### バージョン管理

バージョン固定ファイル: `.python-version`, `uv.lock`

### セットアップ手順

#### macOS

```bash
brew install uv
uv python install 3.12
uv venv .venv
uv sync
```

#### Windows

```powershell
winget install --id astral-sh.uv
uv python install 3.12
uv venv .venv
uv sync
```

#### Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
uv venv .venv
uv sync
```

### 依存関係のインストール

```bash
uv sync
```

### 主要コマンド

```bash
uv run python -m coord_prompt_studio.cli --help
uv run pytest
uv run pytest --cov=src --cov-report=term-missing
uv run ruff check .
uv run ruff format .
uv run basedpyright
```

---

## リポジトリ構造

### ディレクトリ構造

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
│       ├── use_cases/
│       ├── adapters/
│       └── repositories/
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

### 主要ディレクトリの役割

| ディレクトリ / ファイル | 役割 |
|----------------------|------|
| `AGENTS.md` | Codex CLI へのコンテキスト注入（開発プロセス・プロダクト定義・技術スタック・構造） |
| `.steering/` | 作業単位のスペックファイル群（意思決定の履歴として Git 管理） |
| `docs/` | プロジェクト全体の永続ドキュメント（PRD・設計書・ガイドライン等） |
| `prompts/` | Codexへ渡すプロンプトテンプレート、ChatGPT Web UI貼り付け用テンプレート |
| `src/coord_prompt_studio/` | Pythonローカルツール本体 |
| `src/coord_prompt_studio/domain/` | プロンプト部品、評価、試行履歴、合成ルールなどのドメインモデル |
| `src/coord_prompt_studio/use_cases/` | CLIから呼ばれるアプリケーション操作 |
| `src/coord_prompt_studio/adapters/` | Codex CLI/SDK、画像保存など外部境界の実装 |
| `src/coord_prompt_studio/repositories/` | JSON/YAML/SQLiteなど永続化境界の実装 |
| `data/` | ローカル実行時の画像、抽出結果、プロンプト部品、評価履歴の保存先 |
| `templates/layouts/` | Post-MVPの雑誌風コラージュ、コーデ説明画像用のレイアウトテンプレート |
| `tests/` | pytestによるテストコード |
| `.venv/` | ローカルPython仮想環境。Git管理しない |
| `pyproject.toml` | Pythonプロジェクト設定、依存関係、ツール設定 |
| `uv.lock` | uvによる依存関係ロックファイル |

### ファイル配置の判断基準

新しいファイルを作る場合:

- **Codex CLI に常時参照させたい** → `AGENTS.md` の該当セクションを更新
- **今回の作業専用のスペック** → `.steering/YYYYMMDD-xxx/` に配置
- **プロジェクト全体の永続的な定義** → `docs/` に配置
- **アイデア・ブレインストーミング** → `docs/ideas/` に配置
- **Codex/ChatGPT向けプロンプトテンプレート** → `prompts/` に配置
- **アプリケーションコード** → `src/coord_prompt_studio/` に配置
- **テストコード** → `tests/` に配置
- **ローカル実行データ** → `data/` に配置

---

## ワークフロー

<!-- このセクションはハーネス共通のワークフロー定義です。編集しないでください。 -->

### setup-project

「setup-project を実行してください」と依頼された場合:

まずプロダクトの概要・目的・ターゲットユーザーを確認する。内容が確認できたら、`docs/` 配下に以下の 6 ドキュメントを順番に作成する。各ファイルを作成するたびにユーザーの確認を得てから次へ進むこと。

1. `product-requirements.md` — プロダクト要求定義書
2. `functional-design.md` — 機能設計書
3. `architecture.md` — 技術仕様書
4. `repository-structure.md` — リポジトリ構造定義書
5. `development-guidelines.md` — 開発ガイドライン
6. `glossary.md` — ユビキタス言語定義

6 ファイルの作成後、`AGENTS.md` の以下のセクションを実際のプロジェクト内容で更新する:
- プロダクト定義セクション（プロダクト名・目的・docs/ 一覧）
- 技術スタックセクション（技術スタック・OS 別セットアップ手順）
- リポジトリ構造セクション（プロジェクトのディレクトリ構造）

### add-feature

「add-feature を実行してください」と依頼された場合:

まず実装したい機能の名前を確認する。機能名が確認できたら、以下の順で進める:

1. GitHub Issue を作成する（`gh issue create`）
2. `.steering/_template/` をコピーして `.steering/YYYYMMDD-[機能名]/` を作成する
3. `requirements.md` を記入する → ユーザーの確認を得てから次へ
4. `design.md` を記入する → ユーザーの確認を得てから次へ
5. `tasklist.md` を記入する → ユーザーの確認を得てから実装へ
6. フィーチャーブランチを作成し、tasklist.md のタスクを順番に実装する
7. PR を作成してマージする

各ステップで必ずユーザーの確認を得てから次に進むこと。tasklist.md の管理ルール（全タスク完了の原則・スキップ禁止等）は「開発プロセス原則」セクションを参照する。
