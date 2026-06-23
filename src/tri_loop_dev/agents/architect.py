from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from tri_loop_dev.config import settings
from tri_loop_dev.schemas.architect import ArchitectureSchema
from tri_loop_dev.state import AgentState
from tri_loop_dev.utils.llm_factory import get_llm


def architect_node(state: AgentState) -> dict:
    """The Architect Agent: Designs the system based on the PRD."""
    print("--- RUNNING ARCHITECT AGENT ---")

    # Request the complex reasoning model via the factory
    llm = get_llm(model=settings.architect_model)

    # 1. Initialize the universal parser
    parser = PydanticOutputParser(pydantic_object=ArchitectureSchema)

    # 2. Inject the format instructions directly into the prompt
    prompt_template = """
    You are an expert AI Architect. Design the technical architecture
    based on this Product Requirements Document (PRD).

    PRD Context:
    {prd_context}

    {format_instructions}
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["prd_context"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    # 3. Chain the prompt, raw LLM, and parser together
    chain = prompt | llm | parser

    # Extract and serialize the PRD from state
    prd = state.get("prd_json")
    prd_str = prd.model_dump_json() if prd else "No PRD provided."

    try:
        # The chain outputs the validated Pydantic object directly
        arch_output = chain.invoke({"prd_context": prd_str})
        return {
            "architecture_schema": arch_output,
            "current_error": None
        }
    except Exception as err:
        print(f"[Architect Error] Failed to parse output: {err}")
        return {
            "architecture_schema": None,
            "current_error": str(err)
        }
