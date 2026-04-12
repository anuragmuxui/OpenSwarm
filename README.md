# OpenSwarm

OpenSwarm is an **open-source multi-agent AI team** you can run locally (terminal UI) or deploy as an API.

Instead of a single "do-everything" bot, OpenSwarm routes each request to the **right specialist agent** (research, data analysis, docs, slides, images, video, and a virtual assistant) and coordinates the result for you.

Built on [Agency Swarm](https://github.com/VRSEN/agency-swarm) and the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python).

---

## What can I do with it?

Examples you can paste into the terminal UI:

- "Research the current competitive landscape for X, cite sources, and summarize in bullets."
- "Analyze `mnt/data.csv`, find anomalies, and produce a chart plus a short narrative."
- "Create a 6-slide pitch deck about X with a modern theme, then export to PPTX."
- "Draft a professional one-page memo about X and export to PDF."
- "Generate a hero image for my landing page, then create 3 variants."
- "Combine these clips, trim pauses, add captions, and export a final video."

OpenSwarm can also connect to external services (Gmail, Slack, GitHub, etc.) via Composio if you set the optional keys.

---

## Agent Roster

| Agent | What it does |
|---|---|
| **Orchestrator** | Routes every user request to the right specialist(s). Never answers directly — pure coordination. |
| **Virtual Assistant** | Handles everyday tasks: writing, scheduling, messaging, task management. Gains 10,000+ external integrations via [Composio](https://composio.dev) (Gmail, Slack, GitHub, HubSpot, and more). |
| **Deep Research** | Conducts comprehensive, evidence-based web research with citations and balanced analysis. |
| **Data Analyst** | Analyses structured data, builds charts, runs statistical models — all inside an isolated IPython kernel. |
| **Slides Agent** | Generates complete, visually polished HTML slide decks, then exports them to PPTX. |
| **Docs Agent** | Creates formatted Word documents and PDFs from outlines or raw content. |
| **Image Generation Agent** | Generates and edits images using Gemini 2.5 Flash Image / Gemini 3 Pro Image and fal.ai. |
| **Video Generation Agent** | Produces videos via Sora (OpenAI), Veo (Google), and Seedance (fal.ai); also edits and combines clips. |

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Python | 3.10 or newer |
| Node.js | 20 or newer |

Everything else (Python packages, Node.js dependencies, Playwright / Chromium, LibreOffice, Poppler) is installed automatically on first run.

---

## Quick Start

### Option A — Local install (interactive terminal)

```bash
git clone https://github.com/VRSEN/openswarm.git
cd openswarm
python run.py
```

On first run, a setup wizard walks you through choosing a provider and entering your API keys. Everything else (Python packages, Node.js dependencies, Playwright browser) installs automatically.

Once configured, `python run.py` drops you straight into the terminal UI. Outputs and generated files are written to `./mnt/`.

---

### Option B — Docker (API server; no system dependencies required)

Requires [Docker](https://docs.docker.com/get-docker/).

```bash
git clone https://github.com/VRSEN/openswarm.git
cd openswarm
cp .env.example .env        # fill in at least one provider key
docker-compose up --build
```

The FastAPI server starts on `http://localhost:8080`.

---

## Running as an API

```bash
python server.py        # local install
# or
docker-compose up       # Docker
```

Starts a FastAPI server on port **8080**. The agency is exposed at `/open-swarm`.

---

## Configuration

### Provider & model

Set your provider key and optionally override the default model in `.env`:

```env
OPENAI_API_KEY=sk-...

# Optional: override the model used by all agents
DEFAULT_MODEL=gpt-4o
```

The onboarding wizard sets these automatically. You can also edit `.env` directly at any time — see `.env.example` for all options.

### Optional integrations

| Key(s) | Feature unlocked |
|---|---|
| `ANTHROPIC_API_KEY` | Claude models via LiteLLM |
| `COMPOSIO_API_KEY` + `COMPOSIO_USER_ID` | 10,000+ external integrations via Virtual Assistant |
| `SEARCH_API_KEY` | Web search, Scholar search, Product search ([searchapi.io](https://www.searchapi.io)) |
| `GOOGLE_API_KEY` | Gemini image generation/editing, Veo video generation |
| `FAL_KEY` | Seedance video generation, video editing, background removal |
| `PEXELS_API_KEY` | Pexels stock photo search (Slides Agent) |
| `PIXABAY_API_KEY` | Pixabay stock photo search (Slides Agent) |
| `UNSPLASH_ACCESS_KEY` | Unsplash stock photo search (Slides Agent) |

Tools that require a missing key raise a clear error at call time — the agent will tell you what to add.

---

## Adding a New Agent

1. Create a new folder: `my_agent/`
2. Add `my_agent.py` (Agent definition), `instructions.md`, and `tools/`
3. Register the agent in `swarm.py` → `create_agency()`

See the [Agency Swarm docs](https://vrsen.github.io/agency-swarm/) for the full agent creation guide.

---

## Learn More

| Component | Library |
|---|---|
| Multi-agent framework | [Agency Swarm](https://github.com/VRSEN/agency-swarm) |
| LLM runtime | [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) |
| External integrations | [Composio](https://composio.dev) |
| Multi-provider LLM routing | [LiteLLM](https://docs.litellm.ai) |
| API deployment | [FastAPI](https://fastapi.tiangolo.com) + Uvicorn |
| SaaS platform | [Agent Swarm](https://agentswarm.ai) |

---

## License

MIT — see [LICENSE](LICENSE).
