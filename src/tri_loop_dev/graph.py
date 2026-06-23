from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from tri_loop_dev.agents.architect import architect_node
from tri_loop_dev.agents.coder import coder_node
from tri_loop_dev.agents.pm_agent import pm_agent_node
from tri_loop_dev.state import AgentState


def build_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node("pm_agent", pm_agent_node)
    workflow.add_node("architect", architect_node)
    workflow.add_node("coder", coder_node)

    workflow.set_entry_point("pm_agent")

    def pm_routing_logic(state: AgentState) -> str:
        if state.get("prd_json"):
            return "architect"
        return END

    # --- NEW: Architect Guardrail Routing ---
    def architect_routing_logic(state: AgentState) -> str:
        """Ensure the architecture schema exists before coding."""
        if not state.get("architecture_schema"):
            # In a V2, you would route back to 'architect' here
            # with an error message injected into the state.
            print("\n[ERROR] Architect failed to produce valid schema. Halting.")
            return END
        return "coder"

    workflow.add_conditional_edges("pm_agent", pm_routing_logic)

    # Replace the linear edge with the conditional gatekeeper
    workflow.add_conditional_edges("architect", architect_routing_logic)

    workflow.add_edge("coder", END)

    memory = MemorySaver()
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["architect"]
    )

app = build_workflow()
