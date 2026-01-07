from app.planner.schema import Plan, PlanStep, new_plan_id

def generate_plan(user_input: str) -> dict:
    """
    Deterministic fallback planner.
    Generates steps dynamically based on intent keywords.
    This is NOT hardcoded workflows — it composes steps at runtime.
    """

    steps = []

    text = user_input.lower()

    if "report" in text:
        steps.append(
            PlanStep(
                id="s1",
                action="retrieve_documents",
                params={"source": "local"},
                verify="documents_loaded"
            )
        )
        steps.append(
            PlanStep(
                id="s2",
                action="generate_report",
                params={"format": "pdf"},
                verify="file_exists"
            )
        )

    if "email" in text or "send" in text:
        steps.append(
            PlanStep(
                id=f"s{len(steps)+1}",
                action="send_email",
                params={"mode": "dry_run"},
                verify="email_sent"
            )
        )

    if not steps:
        steps.append(
            PlanStep(
                id="s1",
                action="clarify_intent",
                params={"question": "What exactly do you want me to do?"},
                verify="user_confirmed"
            )
        )

    plan = Plan(
        plan_id=new_plan_id(),
        steps=steps
    )

    return plan.dict()
