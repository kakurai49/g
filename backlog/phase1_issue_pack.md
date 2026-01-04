# 0. 今回の前提（Eとして固定する制約）

* **開発の中心**：GitHub（Issue/PR/Actions）＋Codex（コード生成/修正支援）＋iPhone（操作・確認）
* **ローカルPC**：基本使わない
  ただし **リポジトリに入れない成果物（大きいアーティファクト等）**が必要なときのみ、例外的にローカル生成して確認する
* **検証フローの中心**：サーバ上に立てたWebで確認（iPhoneブラウザで触れることが最重要）
* **サーバ運用**：極力「GitHub Actions → 自動デプロイ → Webで動作確認」で完結
  （サーバへの手作業SSHは最小化）

---

# 1. iPhone中心の開発ループ（最初に“観測”を作る）

あなたのやりやすさを最大化するため、Phase1の最初に「**ブラウザからサーバへアクセスして状態を観測できるWeb**」を作ります。
ここを基点に、Issueを進めるたびに **iPhoneで確認 → Issue close** が回ります。

推奨ループ：

1. GitHub Issueを開く（iPhone）
2. CodexにIssue本文を貼って実装案を作る（Codex）
3. PR作成 → GitHub Actions CIが走る（GitHub）
4. mainにマージ → 自動デプロイ（GitHub Actions）
5. iPhoneで **Dev Portal（後述）**を開いて動作確認
6. OKならIssueクローズ

---

# 2. Phase1をS1〜S6に分解（S＝観測観点／A(S)＝Issues）

Phase1の中での観点を、あなたの運用に合わせてこう定義します：

* **S1：iPhone中心の開発・デプロイ観点**
  「iPhoneだけで回る開発導線になっているか？」
* **S2：教材取り込み・閲覧観点**
  「添付理論（MD）がシステムに入り、Webで読めるか？」
* **S3：検索観点**
  「目的箇所に辿れるか？（キーワード＋ベクトル）」
* **S4：RAG Q&A観点**
  「質問→根拠→回答の導線が成立しているか？」
* **S5：練習問題観点**
  「問題を解いて学習ログが溜まるか？」
* **S6：品質・運用観点**
  「壊れにくく、原因が追えるか？（CI/ログ/安全性）」

ここから先は、**各Sをさらに細分化した A(S)＝GitHub Issues** を提示します。

---

# 3. GitHubの運用セット（先に決め打ち）

## Milestone

* `P1 - iPhone-first MVP`

## Labels（最低限）

* `phase:1`
* `S1-devops` `S2-content` `S3-search` `S4-rag` `S5-exercise` `S6-quality`
* `area:api` `area:web` `area:db` `area:infra` `area:llm`
* `priority:p0` `priority:p1`
* `type:feature` `type:chore` `type:docs`

## Issue命名規則

* `[P1-S1-01] ...` のように付番（iPhoneでも追いやすい）

---

# 4. Phase1 Issueパック（S1〜S6細分化）

以下は **Phase1（iPhone-first MVP）** のための、細分化したIssues一式です。
それぞれ **「完了条件（A(S)）」と「iPhoneでの確認方法」**を入れています。

---

## Epic（親Issue）: [P1-S1-00] iPhone中心 開発・デプロイ導線（S1）

**Labels**: `phase:1`, `S1-devops`, `priority:p0`, `type:chore`
**Milestone**: `P1 - iPhone-first MVP`

**Goal**
GitHub→CI→デプロイ→iPhone Web確認 のループを確立する。

**Done（Epic完了条件）**

* mainにマージすると自動デプロイされ、iPhoneで確認できる
* 主要操作がGitHub UIからできる（ローカルPCなし）

### 子Issue（A(S1)）

#### [P1-S1-01] リポジトリ骨格作成（単一サービス構成で開始）

**Labels**: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:chore`
**Done**

* `apps/api`（FastAPI想定）を作成
* `docker/` と `docker-compose.yml`（サーバ用）を作成
* `README.md`に「デプロイされるURL」「動作確認URL（/health等）」を先に書く

**iPhone確認**

* GitHub上でREADMEが入口になっていることを確認

---

#### [P1-S1-02] Issueテンプレ（Codex貼り付け前提）作成

**Labels**: `phase:1`, `S1-devops`, `priority:p1`, `type:chore`
**Done**

* `.github/ISSUE_TEMPLATE/feature.md` 等を作る
* テンプレに以下を含める

  * Context / Scope / Done条件 / iPhone確認方法
  * **Codex Prompt欄**（ここを丸ごと貼る運用）

**iPhone確認**

* iPhoneのGitHubアプリ/ブラウザからIssue作成が楽になっている

---

#### [P1-S1-03] GitHub Actions: CI（lint + unit test）を追加

**Labels**: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:feature`
**Done**

* PR作成でCIが走る
* 少なくとも `python -m compileall` / `pytest` / `ruff`（等）いずれかが動く

**iPhone確認**

* PR画面でChecksが緑になること

---

#### [P1-S1-04] GitHub Actions: Dockerイメージbuild & push（GHCR）

**Labels**: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:feature`
**Done**

* mainマージでコンテナイメージがビルドされ、GHCRへpushされる
* タグに `sha` または `semver` を付ける（ロールバックに必要）

**iPhone確認**

* Actionsログでpush成功を確認（GHCRのPackages一覧でもOK）

---

#### [P1-S1-05] サーバ側：コンテナ起動の最小セット（DBなしでもOK）を立てる

**Labels**: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:feature`
**Done**

* サーバで `docker compose up -d` でアプリが立つ（最初はDB無しでも可）
* `/health` が200を返す

**iPhone確認**

* `https://<your-domain>/health` をSafariで開いてOK

---

#### [P1-S1-06] 自動デプロイ（GitHub Actions→サーバ反映）を確立

**Labels**: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:feature`
**Done（どれか1方式でOK）**

* 方式A：GitHub ActionsからSSHでサーバに入って `docker compose pull && up -d`
* 方式B：サーバがWebHook受けてpull/upする
* 方式C：サーバにself-hosted runnerを置いてdeploy jobを実行する

**iPhone確認**

* mainマージ後に `/version` が新しいcommit SHAを表示する

---

#### [P1-S1-07] 先に“確認用Web”を作る（Dev Portal最小）

**Labels**: `phase:1`, `S1-devops`, `area:web`, `area:api`, `priority:p0`, `type:feature`
**Done**

* `/` または `/dev` に **超簡易ページ**を出す（HTMLでOK）
* そのページが JS fetch で `/health` を叩き結果を表示する
* `/version`（commit SHA/ビルド時刻）も表示する

**iPhone確認**

* iPhoneでページを開き、「API疎通OK」「version表示」が見える

> 以後のIssueは、このDev Portalで“できた/できてない”を毎回確認できます。

---

#### [P1-S1-08] リバースプロキシ + HTTPS（または暫定でも良い）

**Labels**: `phase:1`, `S1-devops`, `area:infra`, `priority:p1`, `type:feature`
**Done**

* `https://` でアクセスできる（Let’s Encrypt/Caddy等）
* 最低限 `/health` と `/dev` が外から見える

**iPhone確認**

* Safariで警告なしに開ける

---

#### [P1-S1-09] 環境変数の管理方針を固定（Secrets含む）

**Labels**: `phase:1`, `S1-devops`, `priority:p1`, `type:docs`
**Done**

* GitHub Secretsに入れるもの（SSH鍵等）
* サーバに置く `.env` の場所
* READMEに「ここを変える」を明記

**iPhone確認**

* READMEに運用手順がある

---

---

## Epic: [P1-S2-00] 教材取り込み・閲覧（S2）

**Labels**: `phase:1`, `S2-content`, `priority:p0`, `type:feature`
**Milestone**: `P1 - iPhone-first MVP`

**Goal**
添付理論MDを取り込み、Webで読める。

### 子Issue（A(S2)）

#### [P1-S2-01] 教材ファイル配置とメタ情報整備

**Labels**: `phase:1`, `S2-content`, `area:infra`, `priority:p0`, `type:chore`
**Done**

* `docs/source/` に理論MDを配置（リポジトリに入れる）
* ファイル名・版（v1.1等）をメタとして扱えるようにする

**iPhone確認**

* GitHubでファイルが見える

---

#### [P1-S2-02] DBスキーマ：doc_chunks（教材チャンク）作成

**Labels**: `phase:1`, `S2-content`, `area:db`, `priority:p0`, `type:feature`
**Done**

* `doc_chunks`（本文、doc_id、章/節、順序、hash、embedding列は後でもOK）
* migrationで作れる

**iPhone確認**

* Dev Portalに「DB接続OK」表示（S6側で作ってもOK）

---

#### [P1-S2-03] “サーバで完結”する取り込み（起動時ブートストラップ）

**Labels**: `phase:1`, `S2-content`, `area:api`, `priority:p0`, `type:feature`
**Done**

* アプリ起動時に `doc_chunks` が空なら自動で取り込み
  （ローカル実行不要＝iPhone運用に合う）
* 再起動で二重登録しない（hashで防止）

**iPhone確認**

* `/dev` に「chunks: N」などの表示が出る

---

#### [P1-S2-04] 教材閲覧API（章・節一覧 / チャンク取得）

**Labels**: `phase:1`, `S2-content`, `area:api`, `priority:p0`, `type:feature`
**Done**

* `GET /api/docs`（章/節のツリー or リスト）
* `GET /api/docs/{doc_id}/chunks?section=...`

**iPhone確認**

* Dev Portalから叩ける or ブラウザでJSONが見える

---

#### [P1-S2-05] Web：教材ビューア（最低限）

**Labels**: `phase:1`, `S2-content`, `area:web`, `priority:p0`, `type:feature`
**Done**

* iPhoneで読みやすい表示（レスポンシブ）
* 章/節を選ぶと本文が表示される（最初はチャンク連結でOK）

**iPhone確認**

* Safariで普通に読める

---

---

## Epic: [P1-S3-00] 検索（S3）

**Labels**: `phase:1`, `S3-search`, `priority:p0`, `type:feature`
**Milestone**: `P1 - iPhone-first MVP`

### 子Issue（A(S3)）

#### [P1-S3-01] キーワード検索（SQL）を先に作る

**Labels**: `phase:1`, `S3-search`, `area:api`, `priority:p0`, `type:feature`
**Done**

* `GET /api/search/keyword?q=...` が `doc_chunks` を返す（TopN）
* 結果に章/節/スニペット/チャンクIDが含まれる

**iPhone確認**

* Web検索画面 or Dev Portalで結果が出る

---

#### [P1-S3-02] pgvector（または代替）の導入判断と採用

**Labels**: `phase:1`, `S3-search`, `area:db`, `priority:p0`, `type:feature`
**Done**

* PostgreSQL + pgvector を使うなら extension有効化まで完了
  （※ iPhone運用なら“サーバで完結する”のが重要）
* 使わないなら代替（簡易TF-IDF等）を一旦採用して明記

**iPhone確認**

* `/dev` に「vector-ready: true」表示（表示はS6でも可）

---

#### [P1-S3-03] embedding生成（doc_chunks用）

**Labels**: `phase:1`, `S3-search`, `area:llm`, `priority:p0`, `type:feature`
**Done**

* 取り込み時 or バッチで embedding を埋める
* 失敗時のリトライ/ログがある

**iPhone確認**

* `/dev` に「embedded: N/M」表示

---

#### [P1-S3-04] ベクトル検索API

**Labels**: `phase:1`, `S3-search`, `area:api`, `priority:p0`, `type:feature`
**Done**

* `GET /api/search/vector?q=...` で近傍チャンクTopKが返る
* スコアと参照メタが返る

**iPhone確認**

* “観測関数 o_S” と検索すると関連節が出る、など

---

#### [P1-S3-05] ハイブリッド検索（keyword + vectorの簡易合成）

**Labels**: `phase:1`, `S3-search`, `area:api`, `priority:p1`, `type:feature`
**Done**

* `GET /api/search?q=...` で統合結果が返る
* 単純なスコア合成でOK（Phase1は完成度より導線）

**iPhone確認**

* “集合被覆”などでそれっぽい節へ辿れる

---

#### [P1-S3-06] Web：検索UI（結果→教材ビューアへジャンプ）

**Labels**: `phase:1`, `S3-search`, `area:web`, `priority:p0`, `type:feature`
**Done**

* 検索→結果一覧→クリックで該当箇所表示

**iPhone確認**

* Safariだけで検索とジャンプができる

---

---

## Epic: [P1-S4-00] RAG Q&A（S4）

**Labels**: `phase:1`, `S4-rag`, `priority:p0`, `type:feature`
**Milestone**: `P1 - iPhone-first MVP`

### 子Issue（A(S4)）

#### [P1-S4-01] Ollama接続ラッパー（タイムアウト/エラー整形）

**Labels**: `phase:1`, `S4-rag`, `area:llm`, `priority:p0`, `type:feature`
**Done**

* Ollamaの接続先をenvで指定できる
* タイムアウト時に分かりやすいエラーが返る

**iPhone確認**

* `/dev` に「ollama: reachable/unreachable」表示

---

#### [P1-S4-02] RAGプロンプトテンプレ（根拠必須・捏造抑制）

**Labels**: `phase:1`, `S4-rag`, `area:llm`, `priority:p0`, `type:feature`
**Done**

* 参照チャンクをコンテキストに入れる
* 回答に「根拠チャンクID（または章/節）」を必ず含める形式にする

**iPhone確認**

* Q&Aで根拠が見える

---

#### [P1-S4-03] RAG回答API（retrieval→回答→根拠返却）

**Labels**: `phase:1`, `S4-rag`, `area:api`, `priority:p0`, `type:feature`
**Done**

* `POST /api/qa`（question）→（answer, citations[]）
* citationsにチャンクID/見出し/スニペット/スコアを含む

**iPhone確認**

* Dev Portalから投げてJSONが返る

---

#### [P1-S4-04] qa_log保存（質問・回答・参照）

**Labels**: `phase:1`, `S4-rag`, `area:db`, `priority:p1`, `type:feature`
**Done**

* 質問と回答と参照チャンクがDBに残る
* 後で一覧できるAPI（簡易）を用意

**iPhone確認**

* “履歴”が見える（簡易でOK）

---

#### [P1-S4-05] Web：Q&A UI（チャット風＋根拠展開）

**Labels**: `phase:1`, `S4-rag`, `area:web`, `priority:p0`, `type:feature`
**Done**

* 質問→回答
* 根拠をタップで展開、タップで教材表示へジャンプ

**iPhone確認**

* Safariで“質問→根拠→教材”が一筆書きで辿れる

---

---

## Epic: [P1-S5-00] 練習問題（S5）

**Labels**: `phase:1`, `S5-exercise`, `priority:p0`, `type:feature`
**Milestone**: `P1 - iPhone-first MVP`

### 子Issue（A(S5)）

#### [P1-S5-01] exercises / attempts スキーマ作成

**Labels**: `phase:1`, `S5-exercise`, `area:db`, `priority:p0`, `type:feature`
**Done**

* `exercises`（問題本文、形式、選択肢、正解、解説、tags）
* `attempts`（exercise_id、回答、正誤、日時）

**iPhone確認**

* `/dev`でテーブル準備OK表示（または簡易APIで確認）

---

#### [P1-S5-02] 初期問題セット（10〜30問）をseedとして投入

**Labels**: `phase:1`, `S5-exercise`, `priority:p0`, `type:feature`
**Done**

* 添付理論のコア（W/E/S/A(S)、観測関数、同値類、集合被覆など）を含む
* seed手段が「サーバで完結」する

  * 起動時seed / 管理API / GitHub Actions手動workflow のどれか

**iPhone確認**

* Webで問題一覧が見える

---

#### [P1-S5-03] 演習API（一覧・取得・解答送信）

**Labels**: `phase:1`, `S5-exercise`, `area:api`, `priority:p0`, `type:feature`
**Done**

* `GET /api/exercises`
* `GET /api/exercises/{id}`
* `POST /api/exercises/{id}/attempt`

**iPhone確認**

* Dev Portalまたはブラウザで動作

---

#### [P1-S5-04] 自動採点（Phase1は“確実に判定できる形式”に限定）

**Labels**: `phase:1`, `S5-exercise`, `area:api`, `priority:p0`, `type:feature`
**Done**

* 選択式：完全一致
* 短答：正規化（空白/全半角/大小）＋許容解リスト
  ※ LLM採点はPhase1では入れない（不安定になりやすい）

**iPhone確認**

* 解いたら即結果が出て履歴に残る

---

#### [P1-S5-05] Web：演習UI（解く→採点→解説）

**Labels**: `phase:1`, `S5-exercise`, `area:web`, `priority:p0`, `type:feature`
**Done**

* iPhoneで解ける入力UI（ボタン中心）
* 採点と解説が表示される

**iPhone確認**

* Safariだけで完結して練習できる

---

#### [P1-S5-06] 学習履歴（直近N件）表示

**Labels**: `phase:1`, `S5-exercise`, `priority:p1`, `type:feature`
**Done**

* 正答率、最近間違えた問題、など最低限の履歴が見える

**iPhone確認**

* “復習”ができる状態

---

---

## Epic: [P1-S6-00] 品質・運用（S6）

**Labels**: `phase:1`, `S6-quality`, `priority:p0`, `type:chore`
**Milestone**: `P1 - iPhone-first MVP`

### 子Issue（A(S6)）

#### [P1-S6-01] /health を“複合ヘルスチェック”にする（DB/LLM）

**Labels**: `phase:1`, `S6-quality`, `area:api`, `priority:p0`, `type:feature`
**Done**

* DB疎通、Ollama疎通、doc_chunks件数、などを返す
* Dev Portalがこの結果を見て表示できる

**iPhone確認**

* `/dev`で状態が一目で分かる

---

#### [P1-S6-02] リクエストログとrequest_id（原因追跡の最小）

**Labels**: `phase:1`, `S6-quality`, `priority:p1`, `type:feature`
**Done**

* すべてのAPIにrequest_id付与
* 例外時にrequest_id付きで返す

**iPhone確認**

* エラー画面にrequest_idが出る

---

#### [P1-S6-03] エラー表示の統一（iPhoneで困らない文言）

**Labels**: `phase:1`, `S6-quality`, `priority:p1`, `type:feature`
**Done**

* “何が足りないか”（DB未接続、Ollama未起動等）がUIに出る

**iPhone確認**

* 詰まったときに次の行動が分かる

---

#### [P1-S6-04] 最低限のアクセス制御（パスワード1個でも良い）

**Labels**: `phase:1`, `S6-quality`, `priority:p1`, `type:feature`
**Done**

* `/dev` や 管理系API（seed/ingestなど）に簡易認証
  （Basic Auth / 共有トークン / IP制限 どれでもOK）

**iPhone確認**

* 外部から丸見えになっていない

---

#### [P1-S6-05] スモークテスト（デプロイ後に自動実行）

**Labels**: `phase:1`, `S6-quality`, `area:infra`, `priority:p0`, `type:feature`
**Done**

* デプロイworkflowの最後に

  * `/health` が200
  * `GET /api/docs` が動く
  * `GET /api/exercises` が動く
    などをチェックして失敗時に分かる

**iPhone確認**

* Actions結果が緑なら最低限OKと言える

---

#### [P1-S6-06] docs/architecture.md（W/E/S/A(S)で書く）

**Labels**: `phase:1`, `S6-quality`, `priority:p0`, `type:docs`
**Done**

* 「iPhone中心のE」「Phase1のS1〜S6」「Issues=A(S)」を書き切る
* Phase2以降の拡張ポイント（obligationタグやset cover導入）をメモ

**iPhone確認**

* README→architectureへの導線があり、見てすぐ分かる

---

---

# 5. 実行順（依存関係つきの最短ルート）

iPhone中心で最短に回す順番はこれです：

1. **S1-01 → S1-03 → S1-04 → S1-05 → S1-06 → S1-07**
   （まず“デプロイできてiPhoneで見える”を作る）
2. **S6-01（/health強化）**
   （観測点が強くなる）
3. **S2-02 → S2-03 → S2-05**
   （教材がWebで読める）
4. **S3-01 →（余力でS3-02〜）→ S3-06**
5. **S4-01 → S4-03 → S4-05**
6. **S5一式**
7. 最後に **S6-05（デプロイ後スモーク）** と **S6-06（設計文書）**

---

# 6. “この設計がG理論に沿っている”ポイント（超短く）

* **W**：リポジトリ＋サーバ＋Webアプリの状態空間
* **E**：iPhone中心／ローカル無し／Webで検証、などの制約
* **S**：S1〜S6（観測観点）
* **A(S)**：各IssueのDone条件（obligation）
* そして **Issueを潰す＝A(S)を満たしていく** になっています。

---
