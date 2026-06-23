from tri_loop_dev.config import settings
from tri_loop_dev.state import AgentState
from tri_loop_dev.utils.llm_factory import get_llm


def coder_node(state: AgentState) -> dict:
    """The Coder Agent: Executes the architectural design step-by-step."""
    print("--- RUNNING CODER AGENT ---")

    # Request the complex reasoning model via the factory
    llm = get_llm(model=settings.coder_model)

    # In a full implementation, the coder reads the architecture schema
    arch_context = state.get("architecture_schema")

    prompt = f"""
    You are an expert ML Developer. Write the implementation code
    strictly following this architecture: {arch_context}

    Return the output as a dictionary where keys are filepaths and
    values are the raw code strings.
    """

    # Note: You may want to bind a Pydantic schema here as well
    # to enforce the dictionary output structure reliably.
    # For now, we invoke raw text generation.
    code_output = llm.invoke(prompt)

    # Parse the output into the expected state dictionary
    # (Assuming the LLM outputs valid code formatting)
    return {"code_artifacts": {"generated_code.py": code_output.content}}
