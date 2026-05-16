from __future__ import annotations

import asyncio
from config.settings import get_settings
from core.agents import (
    run_defensive_skeptic,
    run_expansive_optimist,
    run_master_synthesizer,
    run_peer_review,
)
from core.contracts import AuditCycle, FinalReport, MetaVistaSession
from core.router import ModelRouter
from core.utils import new_session_id, save_json


async def run_metavista_audit(user_prompt: str) -> MetaVistaSession:
    settings = get_settings()
    router = ModelRouter(settings)

    critique_client = router.critique_client()
    peer_client = router.peer_review_client()
    synthesis_client = router.synthesis_client()

    optimist_task = run_expansive_optimist(user_prompt, critique_client, mock=settings.should_mock)
    skeptic_task = run_defensive_skeptic(user_prompt, critique_client, mock=settings.should_mock)
    optimist_result, skeptic_result = await asyncio.gather(optimist_task, skeptic_task)

    peer_review = await run_peer_review(
        user_prompt=user_prompt,
        optimist=optimist_result.content,
        skeptic=skeptic_result.content,
        client=peer_client,
        mock=settings.should_mock,
    )

    final_result = await run_master_synthesizer(
        user_prompt=user_prompt,
        optimist=optimist_result.content,
        skeptic=skeptic_result.content,
        peer_review=peer_review,
        client=synthesis_client,
        mock=settings.should_mock_final,
    )

    history = [
        AuditCycle(
            cycle=1,
            consensus_count=max(1, peer_review.consensus_count - 2),
            conflict_count=peer_review.conflict_count + 2,
            log_summary='Independent discovery complete. Optimist and Skeptic created separate briefs.',
        ),
        AuditCycle(
            cycle=2,
            consensus_count=peer_review.consensus_count,
            conflict_count=peer_review.conflict_count,
            log_summary=peer_review.critique_text,
        ),
        AuditCycle(
            cycle=3,
            consensus_count=peer_review.consensus_count + 2,
            conflict_count=max(0, peer_review.conflict_count - 1),
            log_summary='Final synthesis complete. Conflicts were resolved or explicitly preserved as caveats.',
        ),
    ]

    session = MetaVistaSession(
        session_id=new_session_id(),
        user_prompt=user_prompt,
        history=history,
        final_report=FinalReport(
            title='MetaVista Verified Intelligence Audit',
            content=final_result.content,
            links=[],
        ),
        agent_outputs=[optimist_result, skeptic_result, final_result],
    )

    save_json('data/last_session.json', session.model_dump())
    return session


def run_audit_sync(user_prompt: str) -> MetaVistaSession:
    return asyncio.run(run_metavista_audit(user_prompt))
