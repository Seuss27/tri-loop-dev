from langchain_core.messages import AIMessage

from tri_loop_dev.state import AgentState


def coder_node(state: AgentState) -> dict:
    """Mock Coder node to validate code generation and state updates."""
    print("--- RUNNING CODER NODE (MOCK) ---")

    # Simulate writing the code defined in the mock architecture
    mock_code = {
        "src/string_utils.py": (
            "def reverse_string(s: str) -> str:\n"
            "    return s[::-1]"
        ),
        "src/main.py": (
            "from string_utils import reverse_string\n\n"
            "if __name__ == '__main__':\n"
            "    print(reverse_string('MVP Test'))"
        )
    }

    success_msg = "Code generation complete."

    # Return ONLY the state properties this node is responsible for updating
    return {
        "code_artifacts": mock_code,
        "messages": [AIMessage(content=success_msg)]
    }
