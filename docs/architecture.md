# Architecture (Phase1)

- **W (Why):** Build a minimal, iPhone-first MVP for the G theory learning system that exposes clear observability points.
- **E (End state):** `/health`, `/version`, and `/dev` are reachable after deploy; `/dev` renders in iPhone Safari and surfaces `/health` data.
- **S (Scope):** FastAPI single service, containerized for docker-compose; no database yet, but keep room for future data/RAG integration.
- **A (Approach):** Start with a single FastAPI app exposing JSON endpoints and a lightweight HTML Dev Portal that fetches `/health`. Keep dependencies minimal.
- **S (Signals):** `/dev` shows the health JSON and version on iPhone; CI (ruff + pytest) passes on PRs.

Phase1の最優先は iPhone で観測できる `/dev` を作ること。ここを S1 の観測点とする。
