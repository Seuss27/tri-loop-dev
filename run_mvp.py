from langchain_core.messages import HumanMessage
from langgraph.types import Command  # Required for modern resumption

from tri_loop_dev.graph import app


def run_local_test() -> None:
    print("--- Starting Tri-Loop MVP Test ---")

    config = {"configurable": {"thread_id": "test_mvp_001"}}

    initial_state = {
        "messages": [
            HumanMessage(
                content="Build a lightweight string reverse utility API."
            )
        ]
    }

    print("\n--- Running PM Agent ---")
    for event in app.stream(initial_state, config):
        for node_name, _state_update in event.items():
            # Check for error state immediately
            if _state_update.get("current_error"):
                print(f"[CRITICAL] PM Agent failed: {_state_update['current_error']}")
                return  # Stop the script immediately to prevent further calls
            print(f"Node Executed: {node_name}")

    print("\n--- Workflow Paused for HITL (Human-in-the-Loop) ---")
    current_state = app.get_state(config)

    print("\nValidated PRD Payload:")
    if current_state.values.get("prd_json"):
        prd = current_state.values["prd_json"]
        print(prd.model_dump_json(indent=2))

    input("\nPress Enter to approve PRD and route to Architect -> Coder...")

    print("\n--- Resuming Workflow ---")

    # 1. Manually update the state to record the human approval
    app.update_state(config, {"is_approved": True})

    # 2. Resume using the explicit Command protocol
    for event in app.stream(Command(resume=True), config):
        for node_name, _state_update in event.items():
            print(f"Node Executed: {node_name}")

    print("\n--- Final Workflow State ---")
    final_state = app.get_state(config)

    print("\nGenerated Code Artifacts:")
    code = final_state.values.get("code_artifacts", {})
    for filepath, content in code.items():
        print(f"\n[{filepath}]:\n{content}")


if __name__ == "__main__":
    run_local_test()
