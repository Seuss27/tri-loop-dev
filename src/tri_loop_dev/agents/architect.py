from langchain_core.messages import AIMessage

from tri_loop_dev.schemas.architect import ArchitectureSchema, ModuleDesign
from tri_loop_dev.state import AgentState


def architect_node(state: AgentState) -> dict:
    """Mock Architect node to validate routing and schema enforcement."""
    print("--- RUNNING ARCHITECT NODE (MOCK) ---")

    # Generate a deterministic mock architecture
    mock_architecture = ArchitectureSchema(
        modules=[
            ModuleDesign(
                name="string_utils",
                file_path="src/string_utils.py",
                responsibilities=["Reverse a given string payload"],
                functions=[],
                imports=[]
            )
        ],
        entry_point="src/main.py",
        external_dependencies=[]
    )

    success_msg = "System architecture blueprint generated successfully."

    # Return ONLY the state properties this node is responsible for updating
    return {
        "architecture_schema": mock_architecture,
        "messages": [AIMessage(content=success_msg)]
    }
