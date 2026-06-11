# 開発ガイドライン (Development Guidelines)

## 開発フロー

全ての機能開発・バグ修正はSDD（スペック駆動開発）フローで行う。詳細は `AGENTS.md` の「開発プロセス原則」セクションを参照する。

## 開発環境

devcontainerは使わない。ローカルPythonの `.venv` を使い、依存管理とコマンド実行には `uv` を使う。

### セットアップ

```bash
uv venv .venv
uv sync
```

### 実行

```bash
uv run python -m coord_prompt_studio.cli --help
```

## コーディング規約

### 全般

- ドメインロジックは `src/coord_prompt_studio/domain/` に置き、Codex CLI/SDKやファイルI/Oへ直接依存させない
- ユースケースは `src/coord_prompt_studio/use_cases/` に置き、ドメイン、リポジトリ、アダプタを組み合わせる
- Codex CLI/SDK呼び出しは `src/coord_prompt_studio/adapters/` に閉じ込める
- ローカル実行データ、実在人物画像、生成済み画像、個人プロンプト履歴を不用意にコミットしない
- コメントは「なぜ」を補う場合だけ書く

### Python固有の規約

- 型ヒントを付与する
- `from __future__ import annotations` を使用する
- データモデルは原則として `dataclass` または明示的な型付きクラスで表現する
- ファイル名、関数名、変数名は `snake_case` とする
- `ruff` のチェックとフォーマットに従う

## テスト方針

### テストの基本方針

- ユニットテストはドメインロジックとプロンプト合成ルールを優先する
- Codex CLI/SDK呼び出しはアダプタ境界でモックする
- ローカルファイル保存は一時ディレクトリを使って検証する
- MVP 0では、コーデ抽出結果の保存、ChatGPT比較記録、良かった/悪かった評価記録を重点的にテストする

### テストの命名規則

- テストファイル名: `test_[対象モジュール名].py`
- テスト関数名: `test_[対象]_[条件]_[期待結果]`
- 例: `test_compose_final_prompt_with_negative_prompt_includes_negative_section`

### テスト実行

```bash
uv run pytest
uv run pytest --cov=src --cov-report=term-missing
```

## リントと型チェック

```bash
uv run ruff check .
uv run ruff format .
uv run basedpyright
```

## コミット規約

### コミットメッセージ形式

```
[種別]: [変更内容の要約]

[詳細（任意）]
```

**種別**:
| 種別 | 用途 |
|-----|------|
| `feat` | 新機能追加 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `refactor` | リファクタリング（機能変更なし） |
| `test` | テスト追加・修正 |
| `chore` | ビルド・設定の変更 |

### コミット単位

- 1コミットは1つの論理的な変更にする
- ドキュメント更新と実装変更は、必要に応じて分ける
- WIPコミットはPR作成前に整理する

## PRレビュー基準

### PR作成時のチェックリスト

- [ ] テストが通っている
- [ ] リントエラーがない
- [ ] 型チェックが通っている
- [ ] PR説明に「変更内容」「テスト方法」が記載されている
- [ ] 関連Issueが紐づいている
- [ ] 必要な永続ドキュメントが更新されている

### レビュー観点

- 設計: `docs/architecture.md` のローカルCodexツール方針に沿っているか
- 責務分離: ドメイン、ユースケース、アダプタ、リポジトリが混ざっていないか
- テスト: 重要なドメインルールと保存処理がカバーされているか
- セキュリティ: Codex認証情報や個人画像をアプリが保存・コミットしない設計になっているか
- UX: 最終画像生成用のChatGPT Web UI貼り付けテキストが分かりやすいか

## ドキュメント更新ルール

| 変更の種類 | 更新が必要なドキュメント |
|-----------|----------------------|
| 新機能追加 | `docs/functional-design.md`、`README.md` |
| アーキテクチャ変更 | `docs/architecture.md` |
| ディレクトリ構造変更 | `docs/repository-structure.md`、`AGENTS.md`（リポジトリ構造セクション） |
| 新しいドメイン用語の追加 | `docs/glossary.md` |
| 技術スタック変更 | `docs/architecture.md`、`AGENTS.md`（技術スタックセクション） |
