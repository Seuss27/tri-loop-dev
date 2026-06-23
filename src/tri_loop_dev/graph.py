from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from tri_loop_dev.agents.architect import architect_node
from tri_loop_dev.agents.coder import coder_node
from tri_loop_dev.agents.pm_agent import pm_agent_node
from tri_loop_dev.state import AgentState

# Define strict node names to prevent HITL mismatches
NODE_PM = "pm_agent"
NODE_ARCHITECT = "architect"
NODE_CODER = "coder"


def build_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node(NODE_PM, pm_agent_node)
    workflow.add_node(NODE_ARCHITECT, architect_node)
    workflow.add_node(NODE_CODER, coder_node)

    workflow.set_entry_point(NODE_PM)

    def pm_routing_logic(state: AgentState) -> str:
        if state.get("prd_json"):
            return NODE_ARCHITECT
        return END

    def architect_routing_logic(state: AgentState) -> str:
        """Ensure the architecture schema exists before coding."""
        if not state.get("architecture_schema"):
            print("\n[ERROR] Architect failed to produce valid schema. Halting.")
            return END
        return NODE_CODER

    workflow.add_conditional_edges(NODE_PM, pm_routing_logic)
    workflow.add_conditional_edges(NODE_ARCHITECT, architect_routing_logic)
    workflow.add_edge(NODE_CODER, END)

    memory = MemorySaver()
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=[NODE_ARCHITECT]  # Strongly typed reference
    )

app = build_workflow()
