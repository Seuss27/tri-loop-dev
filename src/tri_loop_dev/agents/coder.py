from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from tri_loop_dev.config import settings
from tri_loop_dev.schemas.coder import CodeArtifacts
from tri_loop_dev.state import AgentState
from tri_loop_dev.utils.llm_factory import get_llm


def coder_node(state: AgentState) -> dict:
    """The Coder Agent: Executes the architectural design step-by-step."""
    print("--- RUNNING CODER AGENT ---")

    llm = get_llm(model=settings.coder_model)

    # 1. Initialize the universal parser with the new schema
    parser = PydanticOutputParser(pydantic_object=CodeArtifacts)

    # 2. Inject format instructions into the prompt
    prompt_template = """
    You are an expert ML Developer. Write the implementation code
    strictly following this architecture:

    Architecture Context:
    {arch_context}

    Do not include conversational filler. Return only the requested structure.

    {format_instructions}
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["arch_context"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    # 3. Chain the prompt, raw LLM, and parser together
    chain = prompt | llm | parser

    # Extract the validated architecture from state
    arch = state.get("architecture_schema")
    arch_str = arch.model_dump_json() if arch else "No architecture provided."

    try:
        # The chain outputs the validated CodeArtifacts object
        code_output = chain.invoke({"arch_context": arch_str})

        # Extract the dictionary of files to update the state
        return {
            "code_artifacts": code_output.files,
            "current_error": None
        }
    except Exception as err:
        print(f"[Coder Error] Failed to parse code output: {err}")
        return {
            "code_artifacts": None,
            "current_error": str(err)
        }
