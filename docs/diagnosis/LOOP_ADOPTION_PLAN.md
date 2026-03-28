# LOOP_ADOPTION_PLAN

## Recommended file layout

```text
/
├─ AGENTS.md
├─ PLANS.md
├─ Plan.md
├─ .agents/
│  └─ skills/
│     ├─ run-required-validations/
│     │  └─ SKILL.md
│     ├─ update-plan-and-log/
│     │  └─ SKILL.md
│     └─ diagnose-failures/
│        └─ SKILL.md
├─ docs/
│  ├─ diagnosis/
│  │  ├─ PROJECT_DIAGNOSIS.md
│  │  └─ LOOP_ADOPTION_PLAN.md
│  └─ improvement/
│     ├─ skills.md
│     └─ loop_requirements_checklist.md
└─ Makefile (optional but strongly recommended)
```

## Required execution order

### Canonical order (must be documented and enforced)
1. Read `PLANS.md`.
2. Create or update `Plan.md`.
3. Implement scope changes (for first loop: `AGENTS.md` + docs/improvement files)。
4. Update `docs/improvement/skills.md` (operation log).
5. Update `docs/improvement/loop_requirements_checklist.md`.
6. Run mandatory validations.
7. If failure: rerun/defer policyを適用してPR本文に明記。

### Enforceability strategy (docs-only)
- `AGENTS.md` 冒頭に「`Plan.md` 更新前に必ず `PLANS.md` を読む」必須ルールを明記。
- PR template にチェック項目追加:
  - `[ ] PLANS.md を先に読んだ`
  - `[ ] Plan.md を更新した`
  - `[ ] skills.md と checklist を更新した`
- `make loop-check`（後続導入）で上記 artefact 存在と更新時刻整合を機械検証。

## Minimal `AGENTS.md` (draft)
- 目的: repo map + 必須順序 + 禁止事項を短く正確に提供。
- 最小項目:
  1. Repo map（`apps/api`, `docs`, `scripts`, `.github/workflows`）
  2. 必須順序: `PLANS.md -> Plan.md -> 実装 -> skills/checklist -> validation`
  3. 必須検証コマンド（現状 + 代替）
  4. 失敗分類ルール（4分類）
  5. defer 許可条件と記録先

## Minimal `PLANS.md` (draft)
- 役割: Plan運用の「規約」だけを記述（計画本体は書かない）。
- 必須項目:
  - Plan.md の目的・粒度（1PR=1主目的）
  - status 定義（todo/in_progress/done/deferred）
  - defer の条件と期限
  - validation 記録フォーマット
  - `skills.md` 追記ルール

## First `Plan.md` candidate

### Goal
初回 loop closure を1PRで成立させる。

### Milestones
1. `AGENTS.md` 初版作成（repo map + order + validation policy）
2. `docs/improvement/skills.md` 初回ログ追加
3. `docs/improvement/loop_requirements_checklist.md` 初版作成
4. 必須検証実行・結果記録
5. PR作成（deferがあれば理由と再実行条件を明記）

### Definition of done
- 上記3ファイルが存在し、相互参照がある
- 必須検証結果がPR本文に記載される
- 失敗がある場合、4分類 + rerun/defer判断を記録

## First PR contents and atomicity rule
- **Atomicity rule**: 初回PRは「loopの土台 artefact とその運用証跡」だけを含め、アプリ機能変更を混ぜない。
- 同梱必須:
  - `AGENTS.md`
  - `Plan.md`（milestone付）
  - `docs/improvement/skills.md`（初回運用ログ）
  - `docs/improvement/loop_requirements_checklist.md`
  - 検証結果セクション（成功/失敗分類つき）

## Mandatory validation commands and rerun/defer policy

### Mandatory commands (target)
1. `make test`
2. `python -m compileall -q app charaname_studio tests`
3. `make loop-check`

### Current-state diagnosis
- `make test`: target未定義（missing instructions / missing docs）
- root compileall: path不整合（code/config inconsistency）
- `make loop-check`: target未定義（missing instructions / missing docs）

### Rerun/defer policy (draft)
- 失敗ごとに必ず次を記録:
  - command
  - timestamp (UTC)
  - classification（4分類）
  - rerun条件
  - defer期限
- defer許可は以下のみ:
  - environment/setup issue
  - flaky or unknown（ただし2回再実行後）
- `missing instructions / missing docs` と `code/config inconsistency` は原則 defer 不可（次PRで即修正計画を必須化）。

## Loop requirements checklist draft
初回版は `docs/improvement/loop_requirements_checklist.md` に次を持つ:
- [ ] `PLANS.md` を先に読んだ記録
- [ ] `Plan.md` に milestone と DoD を記述
- [ ] `AGENTS.md` に order と validation policy を記述
- [ ] `docs/improvement/skills.md` に実行ログ追記
- [ ] 必須3コマンドを実行し結果分類
- [ ] defer があれば理由・期限・owner を記述

## Top skill candidates
1. `run-required-validations`
   - 指定3コマンド実行 + 結果分類 + rerun/defer判定
2. `update-plan-and-log`
   - Plan.md milestone更新と `docs/improvement/skills.md` 記録を同期
3. `loop-pr-assembly`
   - PR本文テンプレ生成（チェックリスト、証跡、defer情報）

## Promotion criteria
- 3回以上繰り返した作業
- 入力/出力が定型
- 失敗分類ルールを機械化できる
- 実行時間を有意に短縮できる

## Suggested automation cadence
- Daily: `make loop-check`（導入後）
- Per PR: required validations + checklist更新
- Weekly: `docs/improvement/skills.md` から skill昇格候補を棚卸し

## 30 / 60 / 90 minute bootstrap plan

### 0-30 min
- `PLANS.md` と `Plan.md` の雛形作成
- `AGENTS.md` 最小版作成（順序ルールと検証方針を明記）

### 30-60 min
- `docs/improvement/skills.md` と checklist 初版作成
- PR template へ loop チェック項目追加

### 60-90 min
- 必須検証3コマンド実行
- 失敗分類・rerun/defer判断記録
- 初回 loop closure PR を作成

## Minimal adoption sequence (single best path)
1. `PLANS.md` を最初に追加（規約を固定）
2. 同PRで `Plan.md` + `AGENTS.md` + `docs/improvement/{skills,checklist}.md` を追加
3. その場で mandatory validation 実行
4. 失敗分類を記録して PR を提出

この順序が最小コストで効果最大。理由は、運用規約（PLANS）を先に固定することで、以降の artefact 作成と検証記録の一貫性を最初から担保できるため。
