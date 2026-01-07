from app.actions_registry import ACTION_REGISTRY
from app.utils.verifier import verify
import time

def execute_step(step: dict) -> dict:
    action = step["action"]
    params = step["params"]
    verify_rule = step["verify"]

    if action not in ACTION_REGISTRY:
        raise Exception(f"Unknown action: {action}")

    # Execute
    result = ACTION_REGISTRY[action](params)

    # Verify
    success = verify(action, result, verify_rule)

    return {
        "action": action,
        "params": params,
        "result": result,
        "verified": success
    }
