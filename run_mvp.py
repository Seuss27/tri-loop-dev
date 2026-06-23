from langchain_core.messages import HumanMessage

from tri_loop_dev.graph import app


def run_local_test() -> None:
    print("--- Starting Tri-Loop MVP Test ---")

    # Define the thread for memory persistence
    config = {"configurable": {"thread_id": "test_mvp_001"}}

    # Initialize state with a sample user request
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
            print(f"Node Executed: {node_name}")

    # The graph is paused here due to interrupt_before=["architect"]
    print("\n--- Workflow Paused for HITL (Human-in-the-Loop) ---")
    current_state = app.get_state(config)

    print("\nValidated PRD Payload:")
    if current_state.values.get("prd_json"):
        # Access the Pydantic model directly to print it
        prd = current_state.values["prd_json"]
        print(prd.model_dump_json(indent=2))

    # Wait for the user to simulate an approval
    input("\nPress Enter to approve PRD and route to Architect -> Coder...")

    print("\n--- Resuming Workflow ---")
    # Streaming with None state resumes the graph from the breakpoint
    for event in app.stream(None, config):
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
