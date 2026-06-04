# Codebase — Long Châu AI Triage Middleware

## Cách chạy prototype

### Cách 1: Docker Compose (khuyến nghị)

```bash
cd codebase
cp .env.example .env
# Điền OPENROUTER_API_KEY vào .env
docker compose up --build
```

- **Long Châu UI (demo chính):** http://localhost:3000
- Chat UI (Streamlit): http://localhost:8501
- API: http://localhost:8000
- Health check: http://localhost:8000/health

### Cách 2: Chạy native (không cần Docker)

**Backend:**
```bash
cd codebase/backend
pip install -r requirements.txt
cp ../.env.example ../.env  # điền API key
BACKEND_URL=http://localhost:8000 uvicorn main:app --reload
```

**Frontend (terminal khác):**
```bash
cd codebase/frontend
pip install -r requirements.txt
BACKEND_URL=http://localhost:8000 streamlit run app.py
```

## Biến môi trường

| Biến | Giá trị mặc định | Mô tả |
|---|---|---|
| `OPENROUTER_API_KEY` | *(bắt buộc)* | API key từ openrouter.ai |
| `OPENROUTER_MODEL` | `openai/gpt-4o-mini` | Model dùng qua OpenRouter |
| `BACKEND_URL` | `http://backend:8000` | URL backend (override khi chạy native) |

## Công cụ và API đã dùng

- **AI:** OpenRouter → `openai/gpt-4o-mini` (3 LLM calls: classifier, answer/gather, handoff summary)
- **Backend:** FastAPI + uvicorn (Python 3.12)
- **Frontend:** Streamlit + Long Châu static shell (vanilla JS)
- **Product search:** Long Châu internal search API (không cần auth)
- **Infrastructure:** Docker Compose (backend + frontend + nginx)
- **HTTP client:** httpx (async)

## Cấu trúc code

```
codebase/
├── backend/
│   ├── main.py              # FastAPI app + /health + /chat endpoint
│   ├── triage.py            # Orchestration: safety_gate → classify → answer/gather/handoff
│   ├── longchau_search.py   # Long Châu product search API (async, trả name/price/url)
│   ├── openrouter_client.py # Thin httpx wrapper cho OpenRouter API
│   ├── prompts.py           # System prompts (classifier, answer, gather, handoff)
│   ├── safety_gate.py       # Keyword list + is_high_risk() — chạy trước classifier
│   └── requirements.txt
├── frontend/
│   ├── app.py               # Streamlit chat UI
│   └── requirements.txt
├── static-shell/            # Long Châu branded demo UI (port 3000)
│   ├── index.html           # Homepage shell (nav, hero, products, footer)
│   ├── chat-widget.js       # Floating chat button + panel, gọi /chat trực tiếp
│   └── assets/
│       └── avatar.png       # Avatar dược sĩ AI
├── nginx/
│   └── nginx.conf           # Serve static-shell trên port 3000
├── docker-compose.yml       # 3 services: backend, frontend (Streamlit), static-shell (nginx)
├── .env.example
├── .gitignore
├── sample-questions.md      # 15 test cases labeled factual/advisory
├── demo-script.md           # Kịch bản demo 4–5 phút
└── triage-test-results.md   # Kết quả test từng case
```

## Phân công

| Thành viên | Phụ trách chính |
|---|---|
| Tiền Anh Kiệt | Scaffold, Docker Compose, demo script, README, UI polish |
| Vũ Đình Phượng | FastAPI backend, Streamlit frontend, Phase 2+3 |
| Nguyễn Văn Phúc | Prompts (classifier, answer, handoff summary), SPEC |
| Nguyễn Hoàng Dương | Sample questions, evidence, test cases |
| Nguyễn Quang Hoà | Test failure paths, triage-test-results.md, dry run |
