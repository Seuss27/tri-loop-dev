from tri_loop_dev.config import settings
from tri_loop_dev.schemas.architect import ArchitectureSchema
from tri_loop_dev.state import AgentState
from tri_loop_dev.utils.llm_factory import get_llm


def architect_node(state: AgentState) -> dict:
    """The Architect Agent: Designs the system based on the PRD."""
    print("--- RUNNING ARCHITECT AGENT ---")

    # Request the complex reasoning model via the factory
    llm = get_llm(model=settings.architect_model)
    structured_llm = llm.with_structured_output(ArchitectureSchema)

    # In a full implementation, you would pass the PRD as context here
    prd_context = state.get("prd_json")

    prompt = f"""
    You are an expert AI Architect. Design the technical architecture
    based on this PRD: {prd_context}
    """

    # Generate the strict architecture schema
    architecture_output = structured_llm.invoke(prompt)

    return {"architecture_schema": architecture_output}
