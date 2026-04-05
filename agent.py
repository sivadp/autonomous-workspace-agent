from toolbox import WorkspaceToolbox
from llm import llm_decide

def run_agent(goal, workspace, max_steps, model):

    toolbox = WorkspaceToolbox(workspace)
    history = []

    for step in range(1, max_steps + 1):

        decision = llm_decide(goal, toolbox, history, step, max_steps, model)

        action = decision.get("action")
        payload = decision.get("payload", {})

        if action == "finish":
            return payload.get("response")

        result = toolbox.execute(action, payload)

        history.append({
            "step": step,
            "action": action,
            "result": result
        })

    return "Step limit reached"