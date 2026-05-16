from .base import AgentSpec


def _extractor(topic, role, prompt, depth):
    return f"""## Information Extraction Agent

**Topic:** {topic or "Not provided"}
**Acting Lens:** {role or "Neutral expert advisor"}
**Depth:** {depth}

### Extracted Task
- Main request: {prompt}
- Required output: advanced research-style answer
- Needs: structure, evidence awareness, recommendations, and final report readiness.

### Decomposition
1. Understand the task.
2. Identify facts, assumptions, constraints, and expected outputs.
3. Separate evidence-backed claims from reasoning.
4. Prepare clean sections for synthesis.
"""


def _reference(topic, role, prompt, depth):
    return """## Reference and Evidence Agent

### Evidence Strategy
- Prefer official docs, primary sources, research papers, and credible technical references.
- Mark unsupported claims clearly.
- Use citations for current facts, laws, prices, model specs, and benchmarks.
- Separate verified evidence from assumptions.

### Citation Plan
| Claim Type | Source Type | Rule |
|---|---|---|
| Definition | official docs/textbook | cite once |
| Current fact | recent web source | cite every claim |
| Technical claim | docs/paper | cite version/date |
| Recommendation | source + reasoning | state assumptions |
"""


def _table(topic, role, prompt, depth):
    return """## Tables and Comparison Agent

### Suggested Tables
| Table | Purpose |
|---|---|
| Agent activation matrix | shows which agents were used and why |
| Evidence quality matrix | separates strong and weak claims |
| Risk table | exposes uncertainty and mitigations |
| Recommendation table | converts research into decisions |
"""


def _visual(topic, role, prompt, depth):
    return """## Visuals and Graph Agent

### Visual Recommendations
- Workflow diagram: prompt → router → agents → synthesis → PDF.
- Agent contribution chart.
- Conflict/consensus telemetry chart.
- Tables or diagrams only when they clarify the answer.
"""


def _skeptic(topic, role, prompt, depth):
    return """## Skeptical Review Agent

### Risks
- Multi-agent output can still hallucinate.
- PDF formatting can make weak research look authoritative.
- Deep research may become slow or expensive.
- Agents may duplicate each other unless prompts are distinct.

### Safeguards
1. Router chooses only relevant agents.
2. Reference agent flags unsupported claims.
3. Synthesizer preserves caveats.
4. Final report separates facts from recommendations.
"""


def _synthesizer(topic, role, prompt, depth):
    return f"""## Master Synthesis Agent

The final output should be a polished advanced report with:
- executive summary
- task framing
- activated agents
- specialist findings
- evidence gaps
- tables/visual suggestions
- final recommendation

Tone: {role or "senior research advisor"}
Depth: {depth}
"""


AGENT_REGISTRY = {
    "extractor": AgentSpec(
        "extractor",
        "Information Extraction Agent",
        "EX",
        "Extracts requirements, entities, assumptions, and constraints.",
        ("extract", "analyze", "research", "summarize", "compare"),
        "Extract structured information.",
        _extractor,
    ),

    "reference": AgentSpec(
        "reference",
        "Reference and Evidence Agent",
        "RF",
        "Plans references, citations, and evidence quality.",
        ("reference", "citation", "source", "paper", "evidence", "latest"),
        "Plan evidence and citations.",
        _reference,
    ),

    "table": AgentSpec(
        "table",
        "Tables and Comparison Agent",
        "TB",
        "Creates tables, matrices, and decision grids.",
        ("table", "compare", "matrix", "pros", "cons", "decision"),
        "Create structured tables.",
        _table,
    ),

    "visual": AgentSpec(
        "visual",
        "Visuals and Graph Agent",
        "VG",
        "Suggests graphs, diagrams, images, and visual outputs.",
        ("graph", "chart", "image", "diagram", "visual", "architecture", "workflow"),
        "Suggest useful visuals.",
        _visual,
    ),

    "skeptic": AgentSpec(
        "skeptic",
        "Skeptical Review Agent",
        "SK",
        "Finds weak assumptions, gaps, risks, and overclaims.",
        ("risk", "validate", "review", "critique", "deep", "advanced"),
        "Critique the work.",
        _skeptic,
    ),

    "synthesizer": AgentSpec(
        "synthesizer",
        "Master Synthesis Agent",
        "MS",
        "Combines all agent outputs into the final report.",
        ("report", "final", "synthesis", "recommend", "deep", "advanced"),
        "Synthesize final answer.",
        _synthesizer,
    ),
}


def select_agents(text: str, depth: str):
    text = f"{text} {depth}".lower()

    selected = [
        a for a in AGENT_REGISTRY.values()
        if any(k in text for k in a.activation_keywords)
    ]

    for key in ["extractor", "skeptic", "synthesizer"]:
        if AGENT_REGISTRY[key] not in selected:
            selected.append(AGENT_REGISTRY[key])

    if depth == "Medium Research":
        if AGENT_REGISTRY["reference"] not in selected:
            selected.append(AGENT_REGISTRY["reference"])

    if depth == "Deep Research":
        for key in ["reference", "table", "visual"]:
            if AGENT_REGISTRY[key] not in selected:
                selected.append(AGENT_REGISTRY[key])

    return selected
