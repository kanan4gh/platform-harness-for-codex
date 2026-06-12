# 設計書

## 実装アプローチ

MVP 0として、Python製CLIからコーディネート画像を指定し、Codex向け抽出プロンプトを実行して、抽出セッションを `data/sessions/` 配下のJSONファイルへ保存する。

実装は、ドメインモデル、ユースケース、アダプタ、リポジトリを分離する。画像入力の検証、抽出結果、ChatGPT比較結果、比較評価はドメイン層の型として表現し、Codex CLI呼び出しとJSONファイルI/Oは外部境界へ閉じ込める。

CLIでは以下の操作を提供する。

1. コーデ画像から抽出セッションを作成する
2. 保存済みセッションへChatGPT抽出結果を追加する
3. 保存済みセッションへ比較評価を追加する
4. セッション一覧を表示する
5. セッション詳細を表示する

抽出のLLM処理は `prompts/coordinate_extraction.md` をテンプレートとして使い、`codex` CLIをsubprocessで呼び出す。テストではCodex呼び出しをモックできるよう、ユースケースは `CodexAdapter` 相当の抽象的な境界へ依存させる。

画像生成APIの呼び出し、最終画像生成プロンプトの合成、人物固定やネガティブ抑制の管理は今回の実装対象外とする。

## 変更対象ファイル

| ファイル | 変更種別 | 内容 |
|---------|---------|------|
| `pyproject.toml` | 新規作成 | Pythonプロジェクト設定、依存関係、ruff、pytest、basedpyright設定を定義する |
| `.python-version` | 新規作成 | Python 3.12系を固定する |
| `.gitignore` | 新規作成 | `.venv/`、キャッシュ、ローカル実行データの不要コミットを防ぐ |
| `prompts/coordinate_extraction.md` | 新規作成 | Codexへ渡すコーデ抽出指示テンプレートを定義する |
| `src/coord_prompt_studio/__init__.py` | 新規作成 | パッケージ初期化 |
| `src/coord_prompt_studio/cli.py` | 新規作成 | TyperベースのCLIエントリポイントを実装する |
| `src/coord_prompt_studio/domain/__init__.py` | 新規作成 | ドメインパッケージ初期化 |
| `src/coord_prompt_studio/domain/sessions.py` | 新規作成 | 抽出セッション、入力画像、抽出結果、比較結果、評価のドメイン型とバリデーションを定義する |
| `src/coord_prompt_studio/use_cases/__init__.py` | 新規作成 | ユースケースパッケージ初期化 |
| `src/coord_prompt_studio/use_cases/extract_coordinate_prompt.py` | 新規作成 | 画像検証、Codex抽出、セッション保存を組み合わせる |
| `src/coord_prompt_studio/use_cases/record_chatgpt_comparison.py` | 新規作成 | ChatGPT抽出結果と比較評価を保存済みセッションへ追加する |
| `src/coord_prompt_studio/use_cases/list_sessions.py` | 新規作成 | 保存済みセッションの一覧と詳細表示用データを取得する |
| `src/coord_prompt_studio/adapters/__init__.py` | 新規作成 | アダプタパッケージ初期化 |
| `src/coord_prompt_studio/adapters/codex.py` | 新規作成 | `codex` CLI subprocess呼び出し境界を実装する |
| `src/coord_prompt_studio/adapters/image_validation.py` | 新規作成 | 画像パス、拡張子、読み込み可能性を検証する |
| `src/coord_prompt_studio/repositories/__init__.py` | 新規作成 | リポジトリパッケージ初期化 |
| `src/coord_prompt_studio/repositories/session_repository.py` | 新規作成 | `data/sessions/` 配下のJSON保存・読み込みを実装する |
| `tests/domain/test_sessions.py` | 新規作成 | ドメイン型、評価値、入力種別、状態遷移を検証する |
| `tests/use_cases/test_extract_coordinate_prompt.py` | 新規作成 | Codex呼び出しをモックして抽出セッション作成を検証する |
| `tests/use_cases/test_record_chatgpt_comparison.py` | 新規作成 | ChatGPT結果と比較評価の追記を検証する |
| `tests/repositories/test_session_repository.py` | 新規作成 | JSON保存・読み込みと一覧取得を一時ディレクトリで検証する |
| `README.md` | 変更 | MVP 0 CLIのセットアップと操作例を追記する |

## 技術的判断と根拠

| 判断 | 根拠 |
|------|------|
| CLIにはTyperを使う | サブコマンド、引数、ヘルプ表示を短い実装で整えられ、MVP後の拡張にも向く |
| セッション保存はJSONファイルにする | MVP 0では検索・集計よりも記録の透明性が重要で、ユーザーが直接確認しやすい |
| セッションIDは日時ベースの安定した文字列にする | ファイル名として扱いやすく、一覧表示でも作成順を追いやすい |
| 画像形式は `.jpg`, `.jpeg`, `.png`, `.webp` を許可する | 実写画像とイラスト画像の一般的な入力形式をMVP範囲でカバーする |
| 画像検証ではPillowを使う | 拡張子だけでなく読み込み可能性を確認でき、破損画像を抽出前に止められる |
| Codex呼び出しはアダプタに隔離する | テストでモックしやすく、将来SDKへ切り替える場合もユースケースを保てる |
| 抽出結果の構造化はMVP 0では緩やかにする | LLM出力の揺れを過度に縛らず、比較検証に必要な貼り付け可能テキストを優先する |
| 比較評価値はドメインで列挙する | `同等`、`不足`、`過剰`、`要改善` 以外の値を保存しないため |
| `data/images/` への画像コピーは行わない | 実在人物画像や第三者画像を不用意に複製・コミットするリスクを下げるため。セッションには参照パスのみ保存する |
| SQLiteは導入しない | 要求のMVP 0範囲ではJSON/YAML優先であり、履歴検索が増えるまで不要 |
| 画像生成APIは呼び出さない | APIコストをかけず抽出・比較ワークフローの検証に集中するため |

## 実装の順序

1. Pythonプロジェクトの最小構成を作成する
2. コーデ抽出プロンプトテンプレートを作成する
3. 抽出セッション関連のドメイン型とバリデーションを実装する
4. JSONセッションリポジトリを実装する
5. 画像検証アダプタを実装する
6. Codex CLIアダプタを実装する
7. コーデ抽出ユースケースを実装する
8. ChatGPT比較結果・比較評価記録ユースケースを実装する
9. セッション一覧・詳細取得ユースケースを実装する
10. CLIサブコマンドを実装する
11. ドメイン、ユースケース、リポジトリのテストを追加する
12. READMEへセットアップと操作例を追記する
13. `pytest`、`ruff check`、`ruff format --check`、`basedpyright` で品質確認する
