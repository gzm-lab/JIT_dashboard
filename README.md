# 📊 JIT Dashboard — Conversational Business Intelligence

> 🧒 **In plain English:** You upload a spreadsheet with numbers, ask a question like "show me the best-selling products", and the app draws a chart for you automatically — no Excel skills needed!

A **natural language BI dashboard** powered by a multi-agent AI pipeline. Ask a question about your data in plain English (or French), and the agent automatically generates, executes, and returns a visualization.

Powered by **DS-STAR** — a multi-agent LLM pipeline (Gemini, OpenAI, or local Ollama) that autonomously analyzes, plans, codes, verifies, and self-debugs.

## ✨ Features

- 💬 **Conversational interface** — ask questions in plain natural language
- 🤖 **DS-STAR multi-agent pipeline** — 7 specialized agents (Analyzer, Planner, Coder, Verifier, Router, Debugger, Finalyzer)
- 📈 **Automatic visualizations** — matplotlib, plotly, seaborn
- 📂 **Multi-format support** — CSV, Excel (.xlsx), JSON
- 🔄 **Auto-debug** — the agent self-corrects its own code errors (up to 3 attempts)
- 🐳 **Dockerized** — one-command deployment

## 🧠 Architecture

```
User (question)
      ↓
 Flask API (/ask)
      ↓
 AgentWrapper
      ↓
 ┌─────────────────────────────────────┐
 │         DS-STAR Pipeline            │
 │                                     │
 │  ANALYZER  → understands the data   │
 │  PLANNER   → plans analysis steps   │
 │  CODER     → generates Python code  │
 │  VERIFIER  → checks the result      │
 │  ROUTER    → adjusts the plan       │
 │  DEBUGGER  → fixes code errors      │
 │  FINALYZER → produces final output  │
 └─────────────────────────────────────┘
      ↓
 exec() → PNG image generated
      ↓
 URL returned → displayed in browser
```

## 🚀 Quick Start

### Option 1 — Docker (recommended)

```bash
git clone https://github.com/gzm-lab/JIT_dashboard.git
cd JIT_dashboard

# Set up environment variables
cp agent/.env.template agent/.env
# Edit agent/.env with your API key (Gemini, OpenAI, or Ollama config)

docker compose up -d
```

The interface is available at **http://localhost:5000**

### Option 2 — Local

```bash
git clone https://github.com/gzm-lab/JIT_dashboard.git
cd JIT_dashboard

pip install -r requirements.txt

# Configure
cp agent/.env.template agent/.env
# Edit agent/.env

# Run
python app/main.py
```

## ⚙️ Configuration

Edit `agent/.env` and `agent/config.yaml`:

```env
# LLM provider selection
GOOGLE_API_KEY=your_gemini_key      # For Gemini (default)
OPENAI_API_KEY=your_openai_key      # For GPT-4
# Ollama: no key required, configure OLLAMA_HOST in config.yaml
```

```yaml
# agent/config.yaml
model: gemini-1.5-flash   # or gpt-4, ollama/llama3

settings:
  max_refinement_rounds: 5
  auto_debug: true
  debug_attempts: 3
  execution_timeout: 60
```

### Supported LLM Providers

| Provider | Model | Variable |
|---|---|---|
| Google Gemini | `gemini-1.5-flash` (default) | `GOOGLE_API_KEY` |
| OpenAI | `gpt-4`, `gpt-4o` | `OPENAI_API_KEY` |
| Ollama (local) | `ollama/llama3`, etc. | none required |

## 📡 API

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Main web interface |
| `POST` | `/ask` | Send a question → receive chart URL |
| `GET` | `/output/<filename>` | Download/display a generated image |
| `GET` | `/health` | Health check |

**Example `/ask` request:**

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me monthly sales as a bar chart"}'

# Response
{"image_url": "/output/chart_abc123.png"}
```

## 📂 Project Structure

```
JIT_dashboard/
├── app/
│   ├── main.py              # Flask — API and web server
│   └── templates/index.html # Chat interface
├── agent/
│   ├── dsstar.py            # DS-STAR multi-agent pipeline (core)
│   ├── agent_wrapper.py     # Flask ↔ DS-STAR bridge
│   ├── config.yaml          # LLM and pipeline configuration
│   ├── prompt.yaml          # Agent prompts
│   ├── provider.py          # LLM provider abstraction
│   └── data/                # Data folder (CSV, XLSX, JSON)
│       └── test.csv         # Sample dataset
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── SETUP_DSSTAR.md          # DS-STAR setup guide
└── architecture.md          # Detailed architecture documentation
```

## 📊 Adding Your Data

Drop your data files into `agent/data/`:

```bash
cp my_data.csv agent/data/
cp sales_report.xlsx agent/data/
```

The agent automatically detects all CSV, XLSX, and JSON files in that folder.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | Python + Flask |
| LLM | Gemini 1.5 Flash / GPT-4 / Ollama |
| Visualization | matplotlib, plotly, seaborn |
| Data processing | pandas, numpy, openpyxl |
| Containerization | Docker + Docker Compose |
