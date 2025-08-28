# AI Voice Agent PoC (Best-Practice Starter)

This starter gives you a **production-minded PoC skeleton** for a 2‑week build using:
- **Frontend:** Next.js (TypeScript) with LiveKit Web SDK
- **Backend:** Python FastAPI (modular, typed), ready for Docker
- **Real-time infra:** LiveKit Cloud (token generation handled server-side)
- **AI:** OpenAI API (stubbed service ready for Realtime/Text pipelines)
- **Auth-ready:** Placeholders for JWT/session; keep secrets in `.env`

> Goal: Ship a *working* PoC quickly while keeping the codebase structured so scaling & security upgrades are easy later.

---

## Monorepo Structure

```
ai-voice-poc-starter/
├─ backend/
│  ├─ app/
│  │  ├─ routers/
│  │  │  ├─ health.py
│  │  │  ├─ tokens.py
│  │  ├─ services/
│  │  │  ├─ livekit_token.py
│  │  │  ├─ openai_client.py
│  │  ├─ core/
│  │  │  ├─ config.py
│  │  │  ├─ logging.py
│  │  ├─ main.py
│  ├─ requirements.txt
│  ├─ Dockerfile
│  ├─ .env.example
├─ frontend/
│  ├─ app/
│  │  └─ page.tsx
│  ├─ lib/api.ts
│  ├─ next.config.js
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ .env.example
│  ├─ Dockerfile
├─ docker-compose.yml
├─ .env.example
└─ README.md
```

---

## Quick Start

### 1) Prereqs
- Node 18+ and npm/pnpm, Python 3.10+
- LiveKit Cloud account (get **API_KEY** and **API_SECRET**, and a **url**)
- OpenAI API key

### 2) Configure env
Copy examples and fill in values:
```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 3) Run backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 4) Run frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

---

## Notes

- **LiveKit tokens** are minted by the backend (`/api/tokens/room`) to keep secrets server-side.
- **OpenAI service** is wrapped in `services/openai_client.py`. You can switch to Realtime later without changing UI.
- Add **auth** later (JWT or NextAuth). Keep the API **stateless**.
- Use **Docker** for parity with production. See `docker-compose.yml`.
