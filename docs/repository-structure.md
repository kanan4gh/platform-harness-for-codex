# リポジトリ構造定義書 (Repository Structure Document)

## ディレクトリ構造

```
[プロジェクトのルートディレクトリ構造を記入]

例（Python プロジェクトの場合）:
project-root/
├── AGENTS.md              # Codex CLI へのコンテキスト注入（開発プロセス・プロダクト定義等）
├── .devcontainer/         # 開発環境定義（Codex CLI インストール済み）
│   ├── devcontainer.json
│   └── postCreate.sh
├── .steering/
│   ├── _template/         # 作業スペックのテンプレート（直接編集しない）
│   └── YYYYMMDD-xxx/      # 作業単位のスペック（機能実装ごとに作成）
├── docs/                  # プロジェクト全体の永続ドキュメント
│   ├── product-requirements.md
│   ├── functional-design.md
│   ├── architecture.md
│   ├── repository-structure.md
│   ├── development-guidelines.md
│   └── glossary.md
├── src/
│   └── myapp/             # アプリケーションのメインコード
├── tests/                 # テストコード
├── .python-version        # Python バージョン固定
├── pyproject.toml         # プロジェクト設定・依存関係
└── README.md
```

## 主要ディレクトリ・ファイルの役割

| パス | 役割 |
|-----|------|
| `AGENTS.md` | Codex CLI への常時コンテキスト注入。プロダクト定義・技術スタック・開発プロセスを含む |
| `.devcontainer/` | 開発環境定義。Codex CLI がインストール済みのコンテナ環境を提供する |
| `.steering/` | 作業単位のスペックファイル群。意思決定の履歴として Git 管理する |
| `.steering/_template/` | スペック作成時のテンプレート。直接編集せず、コピーして使う |
| `docs/` | プロジェクト全体の永続ドキュメント。設計・方針・規約を定義する |
| <!-- 例: `src/` --> | <!-- 例: アプリケーションのメインコード --> |
| <!-- 例: `tests/` --> | <!-- 例: テストコード（pytest） --> |

## ファイル配置の判断基準

新しいファイルを作成する際の配置先:

| 内容 | 配置先 |
|-----|-------|
| Codex CLI に常時参照させたい情報 | `AGENTS.md` の該当セクションを更新 |
| 今回の作業に特化したスペック | `.steering/YYYYMMDD-[機能名]/` に配置 |
| プロジェクト全体の永続的な定義 | `docs/` に配置 |
| アイデア・ブレインストーミングメモ | `docs/ideas/` に配置 |
| アプリケーションのソースコード | `src/` 配下に配置（プロジェクト構造に従う） |
| テストコード | `tests/` 配下に配置 |

## 命名規則

### ファイル名

<!-- 例:
- Python ソースファイル: `snake_case.py`
- テストファイル: `test_[対象モジュール名].py`
- ドキュメント: `kebab-case.md`
-->
[プロジェクトのファイル命名規則を記入]

### ディレクトリ名

<!-- 例: すべて小文字・ハイフン区切り（例: `user-service/`） -->
[プロジェクトのディレクトリ命名規則を記入]

### ブランチ名

<!-- 例:
- 機能追加: `feat/[機能名]`
- バグ修正: `fix/[修正内容]`
- ドキュメント: `docs/[内容]`
-->
[ブランチ命名規則を記入]
