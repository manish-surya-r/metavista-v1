from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any


def new_session_id() -> str:
    return f'mv-session-{int(time.time())}'


def extract_json(text: str) -> dict[str, Any]:
    """Extract the first JSON object from a model response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r'\{.*\}', text, flags=re.DOTALL)
    if not match:
        raise ValueError('No JSON object found in model response')
    return json.loads(match.group(0))


def save_json(path: str | Path, data: dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2), encoding='utf-8')
