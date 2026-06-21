from langchain_anthropic import ChatAnthropic
from tri_loop_dev.schemas.prd import PRDSchema
from tri_loop_dev.state import AgentState


def pm_agent_node(state: AgentState):
    """
    The PM Agent: Responsible for requirements gathering and PRD creation.
    If requirements are incomplete, it requests clarification.
    """
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

    # Bind the Pydantic schema to the LLM so it MUST output JSON
    structured_llm = llm.with_structured_output(PRDSchema)

    prompt = f"""
    You are an expert Product Manager. Your goal is to create a detailed PRD for
    the user's request.

    Current request: {state['messages'][-1].content}

    If the request is missing infrastructure details or clear success criteria,
    do not guess. Instead, populate the 'unresolved_questions' field and keep
    other fields as empty strings or placeholders.
    """

    prd_output = structured_llm.invoke(prompt)

    # Return the update for the AgentState
    return {"prd_json": prd_output}
