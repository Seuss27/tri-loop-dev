from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from tri_loop_dev.config import settings
from tri_loop_dev.schemas.prd import PRDSchema
from tri_loop_dev.state import AgentState
from tri_loop_dev.utils.llm_factory import get_llm


def pm_agent_node(state: AgentState) -> dict:
    """The PM Agent: Responsible for requirements gathering and PRD."""
    print("--- RUNNING PM AGENT ---")

    llm = get_llm(model=settings.pm_model)

    # 1. Initialize the universal parser
    parser = PydanticOutputParser(pydantic_object=PRDSchema)

    # 2. Inject the format instructions directly into the prompt
    prompt_template = """
    You are an expert Product Manager. Your goal is to create a detailed PRD.

    Current request: {request}

    If the request is missing details, populate 'unresolved_questions'
    and keep other fields empty.

    {format_instructions}
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["request"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    # 3. Chain the prompt, raw LLM, and parser together
    chain = prompt | llm | parser

    try:
        # The chain outputs the validated Pydantic object directly
        prd_output = chain.invoke({"request": state["messages"][-1].content})
        return {"prd_json": prd_output, "current_error": None}
    except Exception as e:
        print(f"[PM Agent Error] Failed to parse output: {e}")
        return {"prd_json": None, "current_error": str(e)}
