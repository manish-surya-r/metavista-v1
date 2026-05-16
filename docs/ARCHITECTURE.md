# MetaVista Architecture

## Goal

MetaVista is a Streamlit-based multi-agent research audit engine. It reduces one-model bias by running separate critique agents, comparing their outputs, and producing a final verified report.

## MVP Architecture

```text
User
 ↓
Streamlit Web Interface
 ↓
Workflow Engine
 ↓
Model Router
 ├── Qwen Cloud / TokenRouter → Expansive Optimist Agent
 ├── Qwen Cloud / TokenRouter → Defensive Skeptic Agent
 ├── Qwen Cloud / TokenRouter → Peer Review Agent
 └── Z.ai / GLM → Master Synthesizer Agent
 ↓
Pydantic Data Contract
 ↓
Streamlit Report + Telemetry Dashboard
```

## Component Responsibilities

### Streamlit UI

Files:

- `app.py`
- `ui/components.py`
- `ui/charts.py`

Responsibilities:

- Accept user prompt
- Trigger audit workflow
- Display final Markdown report
- Display telemetry table and line chart
- Display expandable agent outputs

### Workflow Engine

File:

- `core/workflow.py`

Responsibilities:

- Run Expansive Optimist and Defensive Skeptic in parallel
- Run Peer Review after both briefs complete
- Run final Master Synthesizer
- Create the final `MetaVistaSession` object
- Save latest session to `data/last_session.json`

### Agent Layer

Files:

- `core/agents.py`
- `core/prompts.py`

Responsibilities:

- Define agent behavior
- Call selected model client
- Parse peer-review JSON
- Produce agent outputs

### Routing Layer

File:

- `core/router.py`

Responsibilities:

- Use TokenRouter when `USE_TOKENROUTER=true`
- Otherwise use Qwen Cloud for critique and peer-review agents
- Use Z.ai for final synthesis

### Services Layer

Files:

- `services/qwen_client.py`
- `services/zai_client.py`
- `services/tokenrouter_client.py`
- `services/base_openai.py`

Responsibilities:

- Encapsulate API calls
- Keep provider details out of workflow code
- Support OpenAI-compatible chat APIs

### Data Contract

File:

- `core/contracts.py`

Responsibilities:

- Define Pydantic models
- Validate session structure
- Keep backend and frontend aligned

## Data Flow

```text
1. User enters research question.
2. Streamlit sends the prompt to `run_audit_sync()`.
3. Workflow runs Optimist and Skeptic concurrently.
4. Peer Review compares both briefs and returns JSON.
5. Master Synthesizer creates the final Markdown report.
6. Streamlit renders report, telemetry, and audit trail.
```

## Why This Fits a 3-Hour MVP

This architecture avoids databases, queues, authentication, and complex deployment. It keeps the system modular enough to expand later while remaining simple enough to demo quickly.
