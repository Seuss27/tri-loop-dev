from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from tri_loop_dev.agents.architect import architect_node
from tri_loop_dev.agents.coder import coder_node
from tri_loop_dev.state import AgentState

from tri_loop_dev.agents.pm_agent import pm_agent_node


def build_workflow():
    workflow = StateGraph(AgentState)

    # 1. Define Nodes
    workflow.add_node("pm_agent", pm_agent_node)
    workflow.add_node("architect", architect_node)
    workflow.add_node("coder", coder_node)

    # 2. Define Entry Point
    workflow.set_entry_point("pm_agent")

    # 3. Define Conditional Logic
    def routing_logic(state: AgentState):
        # If we have a validated PRD, move to architect
        if state.get("prd_json"):
            return "architect"
        return END

    workflow.add_conditional_edges("pm_agent", routing_logic)

    # 4. Define Linear Workflow
    workflow.add_edge("architect", "coder")
    workflow.add_edge("coder", END)

    # 5. Compile with Checkpointing (Enables HITL)
    memory = MemorySaver()
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["architect"] # Pause here for your approval
    )

app = build_workflow()
