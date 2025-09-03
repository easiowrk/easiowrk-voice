# EasioWrk Voice

This starter gives you a **production-minded PoC skeleton** for a 2‑week build using:
- **Frontend:** Next.js (TypeScript) with LiveKit Web SDK
- **Backend:** Python FastAPI
- **Real-time infra:** LiveKit Cloud 
- **AI:** OpenAI API 

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
