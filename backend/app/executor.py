from app.actions_registry import ACTION_REGISTRY
from app.utils.verifier import verify

def resolve_params(params, context):
    resolved = {}
    for k, v in params.items():
        if isinstance(v, str) and v.startswith("$"):
            step_id, field = v[1:].split(".")
            resolved[k] = context[step_id][field]
        else:
            resolved[k] = v
    return resolved

def execute_plan(plan):
    context = {}

    for step in plan["steps"]:
        action = step["action"]
        verify_rule = step["verify"]

        params = resolve_params(step["params"], context)

        result = ACTION_REGISTRY[action](params)
        success = verify(action, result, verify_rule)

        context[step["id"]] = result

        if not success:
            return {
                "status": "paused",
                "failed_step": step,
                "context": context
            }

    return {
        "status": "completed",
        "context": context
    }
