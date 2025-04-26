```markdown
# 🧸  Inhyung-Calculator (Doll Calculator)

> **Inventory & winner tracker for claw-machines**  
> REST API ＋ ChatGPT Function Calling ＋ MCP Server

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Why?

Claw-machine (UFO catcher) shops still manage stock and win counts in Excel.  
The **Doll Calculator** turns those manual sheets into a lightweight API that:

* keeps per-machine stock & win stats in real time  
* lets employees update data with one curl / webhook  
* answers owners’ natural-language questions via ChatGPT

---

## 🎯 Key Features

| Category | Details |
|----------|---------|
| **REST API** | `POST /restock`, `POST /win`, `GET /status`, `GET /ranking` |
| **ChatGPT Plug-in** | JSON Schema → automatic function calling |
| **MCP Server** | FastMCP wrapper for stdin / SSE transport |
| **Portable Data** | Single `machines.json`, easy to swap for SQLite |
| **Docker-ready** | `docker run -p 5000:5000 inhyung-calculator` |

---

## 🛠️ Tech Stack
* **Python 3.10**  · Flask 1.1  
* **FastMCP**  (MCP Server helper)  
* **OpenAI ChatCompletion** (Function calling)  
* Docker (optional deployment)

---

## ⚡ Quick Start

```bash
# 1. clone & install
git clone https://github.com/oss2025/inhyung-calculator.git
cd inhyung-calculator
pip install -r requirements.txt

# 2. run server
python app.py     # → 0.0.0.0:5000

# 3. restock example
curl -X POST http://localhost:5000/restock \
     -H "Content-Type: application/json" \
     -d '{"machine_id":"1","item_name":"Pikachu","quantity":10}'
```

Docker one-liner:

```bash
docker build -t inhyung-calculator .
docker run -p 5000:5000 inhyung-calculator
```

---

## 🔌 API Reference

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| `POST` | `/restock` | `{machine_id, item_name, quantity}` | add stock |
| `POST` | `/win` | `{machine_id, item_name}` | add 1 win & reduce stock |
| `GET` | `/status` | `?machine_id=` | current list, stock, wins |
| `GET` | `/ranking` | `?machine_id=&top_n=` | top sellers |

> All responses are JSON.   HTTP 4xx = validation errors.

---

## 🤖 ChatGPT Function Schema (excerpt)

```jsonc
{
  "name": "get_machine_status",
  "description": "Return current dolls & wins for a specific machine",
  "parameters": {
    "type": "object",
    "properties": {
      "machine_id": { "type": "string" }
    },
    "required": ["machine_id"]
  }
}
```

Once imported, ChatGPT can answer:

> **Q:** “How many Pikachu are left in machine 2?”  
> **A:** “Machine 2 still has *8* Pikachu with *2* wins recorded.”

---

## 🗂 Project Structure

```
app.py               # Flask routes
mcp_server.py        # FastMCP wrapper
data/machines.json   # default dataset
schemas/             # OpenAI function schemas
tests/               # pytest cases
Dockerfile
```

---

## 🛣 Roadmap

- [ ] Daily e-mail report (`schedule` module)  
- [ ] Multi-shop tenancy (SQLite)  
- [ ] React dashboard (Recharts)  
- [ ] Webhook alerts when stock < threshold

---

## 🤝 Contributing

1. Fork the repo & create a feature branch.  
2. Commit following **Conventional Commits**; open a PR.  
3. Ensure `pytest -q` passes.  
We love PRs ≥ 21 commits 😉.

---

## 📜 License

MIT © 2025  OSS Team 42

Enjoy your stress-free claw-machine management!
```
