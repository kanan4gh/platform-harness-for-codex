# 技術仕様書 (Architecture Document)

## システム概要

Coord Prompt Studio（仮称）は、画像生成プロンプトを複数のプロンプト部品として管理し、段階的に最終プロンプトへ合成するローカルツールとして設計する。MVP 0〜2では、Codex CLIまたはCodex SDKを実行基盤として使い、ユーザーのChatGPT/Codex認証でコーデ抽出、プロンプト改善、振り返り記録を行う。

最終画像生成はアプリ内で実行しない。ユーザーが元画像と最終プロンプトをChatGPT Web UIへ貼り付け、生成結果を必要に応じてローカルツールへ戻して評価・記録する。

## アーキテクチャ図

```text
┌────────────────────────────────────────────┐
│              Local Tool UI                 │
│ CLI / TUI / future local web UI            │
│ 画像入力 / プロンプト部品 / 比較 / 振り返り    │
└─────────────────────┬──────────────────────┘
                      │
┌─────────────────────▼──────────────────────┐
│          Application Use Cases              │
│ coordinate extraction / prompt composition  │
│ review tracking / variation planning        │
└─────────────────────┬──────────────────────┘
                      │
┌─────────────────────▼──────────────────────┐
│              Domain Layer                   │
│ PromptPart / FinalPrompt / Feedback / Trial │
└─────────────┬────────────────────┬──────────┘
              │                    │
┌─────────────▼─────────────┐ ┌────▼────────────────┐
│       Local Data Store     │ │    Codex Adapter     │
│ files / SQLite             │ │ Codex CLI / SDK      │
│ prompt parts / feedback    │ │ ChatGPT/Codex auth   │
└─────────────┬──────────────┘ └─────────┬───────────┘
              │                          │
              │                          ▼
              │              ┌────────────────────────┐
              │              │ ChatGPT Web UI          │
              │              │ final image generation  │
              │              └────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────┐
│ Post-MVP Layout / Collage Output           │
└────────────────────────────────────────────┘
```

## 技術スタック

MVP 0〜2は、Codex CLIまたはCodex SDKを使うローカルツールとして実装する。Pythonはローカルツールの実装、永続化、Codex SDK連携、画像ファイル操作に使う。Webアプリ化は将来の選択肢とする。

| カテゴリ | 採用技術 | 選定理由 |
|---------|---------|---------|
| 実行基盤 | Codex CLI / Codex SDK | ChatGPT/Codexログインを利用し、APIキー課金を前提にしない |
| 言語 | Python 3.12+ | ローカルCLI、ファイル処理、Codex SDK連携、将来の画像処理に向く |
| 仮想環境 | venv（`.venv`） | devcontainerを使わず、ローカルに明示的なPython仮想環境を作って動かせる |
| 依存管理 | uv + pyproject.toml + uv.lock | `.venv` を使いながら、依存解決とロックファイル管理を高速かつ再現可能にできる |
| CLI | Typer または argparse | MVP 0の操作を小さく始められる |
| Codex連携 | `codex` CLI subprocess / `openai-codex` Python SDK | まずCLIで単純に始め、必要に応じてSDKへ移行できる |
| データストア | JSON/YAML files → SQLite | MVP 0はファイルで十分。履歴検索が増えたらSQLiteへ移行する |
| 画像保存 | ローカルファイルシステム | 入力画像と生成済み画像をユーザーの作業ディレクトリで管理できる |
| テスト | pytest | ドメインロジック、永続化、プロンプト合成を検証しやすい |
| リンター/整形 | ruff | Pythonコード品質を保つ |
| 型チェック | basedpyright または pyright | データモデルとユースケースの型安全性を高める |

## レイヤー構成

### Local Tool UI

**役割**:
- ユーザー操作を受け取り、ユースケースを呼び出す
- MVP 0ではCLIで開始し、必要に応じてTUIまたはローカルWeb UIへ拡張する

**主な操作**:
- コーデ画像を指定してコーデ抽出を実行する
- ChatGPT比較用の抽出結果を入力する
- 良かった/悪かったを記録する
- MVP 1以降でプロンプト部品を登録・合成する
- 最終画像生成用の貼り付けテキストを出力する

### Application Use Cases

**役割**:
- UIから呼ばれる操作を定義する
- ドメインモデル、ローカル保存、Codex Adapterを組み合わせる

**主なユースケース**:
- `extract_coordinate_prompt`
- `record_chatgpt_comparison`
- `record_review`
- `save_prompt_part`
- `compose_final_prompt`
- `suggest_prompt_improvements`
- `create_variation_prompt`

### Domain Layer

**役割**:
- プロンプト部品、合成、評価、試行履歴のルールを表現する
- Codex CLI/SDKやファイル保存に依存しない純粋なロジックを置く

**主なドメインサービス**:
- `PromptPartService`
- `PromptComposer`
- `FeedbackClassifier`
- `TrialHistoryService`
- `LayoutTemplateService`

### Local Data Store

**役割**:
- プロンプト部品、抽出セッション、比較結果、振り返り評価、生成済み画像メタ情報を保存する

**保存対象**:
- 画像メタ情報
- コーデ抽出プロンプト
- ChatGPT比較結果
- 良かった/悪かった評価
- プロンプト部品
- 試行履歴
- 将来的なレイアウトテンプレート

### Codex Adapter

**役割**:
- Codex CLIまたはCodex SDKを呼び出す
- 画像と指示文をCodexへ渡し、構造化された抽出結果や改善案を受け取る
- Codex認証はユーザーの既存ログインに委ねる

**実装方針**:
- MVP 0では `codex exec` または対話中のCodex CLIでコーデ抽出を実行する
- 自動化が必要になった段階で `openai-codex` Python SDKを検討する
- Codexセッション、プロンプトテンプレート、出力スキーマはリポジトリ内で管理する

## 主要コンポーネント

### Coordinate Extraction

**役割**:
コーデ画像からコーデ抽出プロンプトを生成する。

**主要ファイル案**:
- `src/coord_prompt_studio/use_cases/extract_coordinate_prompt.py` — MVP 0の抽出ユースケース
- `src/coord_prompt_studio/domain/prompt_parts.py` — コーデ抽出プロンプトのドメイン型
- `src/coord_prompt_studio/adapters/codex.py` — Codex CLI/SDK呼び出し境界
- `prompts/coordinate_extraction.md` — Codexへ渡す抽出指示

**依存関係**:
- `CodexAdapter`
- `PromptPartRepository`
- `FeedbackRepository`

---

### ChatGPT Comparison

**役割**:
本プロダクトの抽出結果と、ユーザーがChatGPTで得た抽出結果を比較し、主観評価を保存する。

**主要ファイル案**:
- `src/coord_prompt_studio/use_cases/record_chatgpt_comparison.py` — 比較記録
- `src/coord_prompt_studio/domain/feedback.py` — 良かった/悪かった評価と理由カテゴリ

**依存関係**:
- `FeedbackRepository`
- `TrialHistoryRepository`

---

### Prompt Parts

**役割**:
人物固定、コーデ抽出、背景、撮影、ポーズ、ネガティブ抑制の各プロンプト部品を管理する。

**主要ファイル案**:
- `src/coord_prompt_studio/domain/prompt_parts.py` — プロンプト部品の型とルール
- `src/coord_prompt_studio/repositories/prompt_parts.py` — 保存と読み出し

**依存関係**:
- `PromptPartRepository`

---

### Prompt Composition

**役割**:
選択されたプロンプト部品を結合し、ChatGPT Web UI貼り付け用の最終プロンプトを生成する。

**主要ファイル案**:
- `src/coord_prompt_studio/domain/prompt_composition.py` — 合成ルール
- `src/coord_prompt_studio/use_cases/compose_final_prompt.py` — 最終プロンプト生成
- `prompts/final_prompt_template.md` — 貼り付け用テンプレート

**依存関係**:
- `PromptPartRepository`
- `TrialHistoryRepository`

---

### Feedback and Trial History

**役割**:
良かった/悪かった、理由カテゴリ、自由記述、試行種別、やり直し回数を記録する。

**主要ファイル案**:
- `src/coord_prompt_studio/domain/feedback.py` — 主観評価モデル
- `src/coord_prompt_studio/domain/trials.py` — 試行履歴モデル
- `src/coord_prompt_studio/use_cases/record_review.py` — 振り返り記録

**依存関係**:
- `FeedbackRepository`
- `TrialHistoryRepository`

---

### Variation

**役割**:
背景、撮影、ポーズの抽出・選択・編集を行い、気に入った画像からの派生生成を支援する。

**主要ファイル案**:
- `src/coord_prompt_studio/domain/variation.py` — 候補と派生生成のルール
- `src/coord_prompt_studio/use_cases/create_variation_prompt.py` — 派生プロンプト生成

**依存関係**:
- `PromptPartRepository`
- `TrialHistoryRepository`

---

### Layout Template

**役割**:
Post-MVPで、雑誌風コラージュやコーデ説明画像のテンプレートを読み込み、画像を配置する。

**主要ファイル案**:
- `src/coord_prompt_studio/domain/layout_template.py` — レイアウトテンプレート定義
- `src/coord_prompt_studio/use_cases/create_collage.py` — コラージュ生成

**依存関係**:
- `LayoutTemplateRepository`
- `ImageStorage`

## データモデル

### PromptPart

```python
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class PromptPartKind(StrEnum):
    COORDINATE = "coordinate"
    PERSON_IDENTITY = "person_identity"
    NEGATIVE = "negative"
    BACKGROUND = "background"
    SHOOTING = "shooting"
    POSE = "pose"


class PromptPartSource(StrEnum):
    IMAGE_EXTRACTION = "image_extraction"
    USER_INPUT = "user_input"
    PRESET = "preset"
    CODEX_SUGGESTION = "codex_suggestion"
    MANUAL_EDIT = "manual_edit"


@dataclass(frozen=True)
class PromptPart:
    id: str
    kind: PromptPartKind
    title: str
    body: str
    source: PromptPartSource
    source_image_id: str | None
    created_at: datetime
    updated_at: datetime
```

### ImageAsset

```python
class ImagePurpose(StrEnum):
    COORDINATE_REFERENCE = "coordinate_reference"
    PERSON_REFERENCE = "person_reference"
    GENERATED_RESULT = "generated_result"
    COLLAGE_OUTPUT = "collage_output"


class ImageStyle(StrEnum):
    PHOTO = "photo"
    ANIME_ILLUSTRATION = "anime_illustration"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ImageAsset:
    id: str
    purpose: ImagePurpose
    style: ImageStyle
    path: str
    mime_type: str
    created_at: datetime
```

### ExtractionSession

```python
@dataclass(frozen=True)
class ExtractionSession:
    id: str
    coordinate_image_id: str
    image_style: ImageStyle
    extracted_prompt_part_id: str
    chatgpt_comparison_text: str | None
    created_at: datetime
```

### Feedback

```python
class SubjectiveRating(StrEnum):
    GOOD = "good"
    BAD = "bad"


class TrialKind(StrEnum):
    FAILED_REGENERATION = "failed_regeneration"
    SUCCESSFUL_DERIVATIVE = "successful_derivative"
    COMPARISON_VARIATION = "comparison_variation"


@dataclass(frozen=True)
class Feedback:
    id: str
    rating: SubjectiveRating
    reasons: list[str]
    note: str | None
    target_type: str
    target_id: str
    trial_kind: TrialKind | None
    created_at: datetime
```

### FinalPrompt

```python
@dataclass(frozen=True)
class FinalPrompt:
    id: str
    prompt_part_ids: list[str]
    positive_prompt: str
    negative_prompt: str | None
    paste_text: str
    created_at: datetime
    updated_at: datetime
```

## 外部依存・連携

| 外部サービス / ツール | 用途 | 認証方式 |
|----------------------|------|---------|
| Codex CLI / Codex SDK | MVP 0〜2のコーデ抽出、改善提案、プロンプト生成 | ユーザーのChatGPT/Codexログイン、またはCodexがサポートする認証 |
| ChatGPT Web UI | 最終画像生成 | ユーザー自身のChatGPTログイン |
| 画像生成API | Post-MVPのアプリ内画像生成 | 未定 |

## セキュリティ考慮事項

- MVP 0〜2ではOpenAI APIキーを前提にしない
- Codexの認証情報はCodex CLI/SDKの管理に委ね、本プロダクトが直接保存しない
- ChatGPTのWebセッションCookieや認証情報を本プロダクトが取得・保存・代理利用しない
- 画像ファイルはローカル保存を基本とし、クラウド保存を導入する場合は明示的なユーザー同意を必要とする
- 実在人物や第三者の画像を扱う場合、利用権限・同意・肖像権への注意喚起をUI上で行う
- レイアウトテンプレートを外部ファイルとして読み込む場合、スクリプト実行を許可せず、データ定義としてのみ扱う

## パフォーマンス考慮事項

- MVP 0では、画像入力から抽出結果表示まで30秒以内を目標とする
- 大きな画像はCodexへ渡しやすいサイズへ事前にリサイズできるようにする
- ローカル履歴が増えた場合、JSON/YAML保存からSQLiteへ移行する
- 画像生成APIはMVP 0〜3では呼び出さないため、生成処理の待機時間は初期パフォーマンス目標に含めない
