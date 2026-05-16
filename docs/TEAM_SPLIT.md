# MetaVista 3-Hour Team Split

Team size: 4 people

- 1 AI Engineer
- 2 Backend Engineers
- 1 Frontend Engineer

## Team Roles

### 1. AI Engineer

Owns:

- `core/prompts.py`
- `core/agents.py`
- Agent behavior
- Prompt quality
- Output quality testing

Tasks:

- Tune Expansive Optimist prompt
- Tune Defensive Skeptic prompt
- Tune Peer Review JSON prompt
- Tune Master Synthesizer prompt
- Ensure final report is clear and useful
- Test 3–5 example prompts

### 2. Backend Engineer 1

Owns:

- `services/base_openai.py`
- `services/qwen_client.py`
- `services/zai_client.py`
- `services/tokenrouter_client.py`
- `config/settings.py`

Tasks:

- API key loading
- Qwen Cloud client
- Z.ai client
- Optional TokenRouter client
- Mock fallback behavior
- Provider error handling

### 3. Backend Engineer 2

Owns:

- `core/contracts.py`
- `core/workflow.py`
- `core/router.py`
- `core/utils.py`

Tasks:

- Pydantic data contract
- Parallel agent execution
- Peer-review parsing
- Session object creation
- Save latest output JSON
- Ensure telemetry history is valid

### 4. Frontend Engineer

Owns:

- `app.py`
- `ui/components.py`
- `ui/charts.py`

Tasks:

- Streamlit layout
- Prompt input
- Run Audit button
- Final report rendering
- Telemetry table
- Consensus/conflict line chart
- Expandable audit trail sections

## 3-Hour Build Timeline

### 0:00–0:30 — Setup

- Create repo
- Create virtual environment
- Install requirements
- Add `.env` from `.env.example`
- Confirm Streamlit launches

### 0:30–1:15 — Core Implementation

- Backend Engineer 1 builds API clients
- Backend Engineer 2 builds contracts and workflow skeleton
- AI Engineer finalizes prompts
- Frontend Engineer creates UI shell

### 1:15–2:00 — Integration

- Connect UI to workflow
- Connect workflow to agents
- Connect agents to Qwen/Z.ai or mock mode
- Add TokenRouter optional routing

### 2:00–2:40 — Demo Polish

- Add telemetry table
- Add line chart
- Add audit trail expanders
- Add sample prompts
- Test mock mode
- Test API mode if keys are available

### 2:40–3:00 — Final Demo Prep

- Run end-to-end
- Fix visible bugs
- Prepare 1 strong demo question
- Explain architecture clearly

## MVP Rule

Do not add login, database, PDF upload, web scraping, auth, billing, user management, or background jobs in the first 3 hours.

The goal is a working multi-agent audit demo, not a complete production platform.
