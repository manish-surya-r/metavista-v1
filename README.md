# MetaVista

MetaVista is a Streamlit-based multi-agent research and reasoning audit engine.

It runs:

1. Expansive Optimist Agent
2. Defensive Skeptic Agent
3. Peer Review Agent
4. Master Synthesizer Agent

The MVP uses Python, Streamlit, Qwen Cloud, Z.ai, and optional TokenRouter.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

If API keys are missing, the app runs in mock mode automatically.

## Environment Variables

```bash
QWEN_API_KEY=
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus

ZAI_API_KEY=
ZAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
ZAI_MODEL=glm-4-plus

TOKENROUTER_API_KEY=
TOKENROUTER_BASE_URL=
TOKENROUTER_MODEL=qwen-plus
USE_TOKENROUTER=false

MOCK_MODE=false
```

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Team Split

See [`docs/TEAM_SPLIT.md`](docs/TEAM_SPLIT.md).

## Project Structure

```text
metavista/
├── app.py
├── README.md
├── .env.example
├── requirements.txt
├── config/
│   ├── __init__.py
│   └── settings.py
├── core/
│   ├── __init__.py
│   ├── contracts.py
│   ├── prompts.py
│   ├── agents.py
│   ├── router.py
│   ├── workflow.py
│   └── utils.py
├── services/
│   ├── __init__.py
│   ├── base_openai.py
│   ├── qwen_client.py
│   ├── zai_client.py
│   └── tokenrouter_client.py
├── ui/
│   ├── __init__.py
│   ├── components.py
│   └── charts.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── TEAM_SPLIT.md
└── data/
```

## Product Flow

```text
User Prompt
 ↓
Streamlit UI
 ↓
Workflow Engine
 ↓
Parallel Critique Agents
 ↓
Peer Review JSON
 ↓
Master Synthesis
 ↓
Final Report + Telemetry
```

## Notes

- Use Qwen Cloud for critique agents.
- Use Z.ai / GLM for final synthesis.
- Use TokenRouter only when you want routing, fallback, or multi-model cost control.
- Keep the first MVP simple.
