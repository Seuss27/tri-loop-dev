from tri_loop_dev.agents.pm_agent import pm_agent_node
from tri_loop_dev.schemas.prd import PRDSchema


def test_pm_agent_node_success(
    mocker, mock_initial_state: dict, valid_prd_object: PRDSchema
) -> None:
    """Test PM agent successfully parsing LLM output into state."""

    # Mock the LLM factory to return a dummy LLM
    mocker.patch("tri_loop_dev.agents.pm_agent.get_llm")

    # Mock the chain.invoke to simulate a successful LLM generation & parse
    mock_invoke = mocker.patch(
        "langchain_core.runnables.base.RunnableSequence.invoke"
    )
    mock_invoke.return_value = valid_prd_object

    # Run the node
    result = pm_agent_node(mock_initial_state)

    # Validate the state updates
    assert result["current_error"] is None
    assert result["prd_json"] == valid_prd_object

    # Ensure it extracted the right message from the state
    mock_invoke.assert_called_once_with(
        {"request": "Build a string reverse API."}
    )


def test_pm_agent_node_parsing_error(mocker, mock_initial_state: dict) -> None:
    """Test PM agent handles LLM hallucination/parsing errors gracefully."""

    mocker.patch("tri_loop_dev.agents.pm_agent.get_llm")

    # Simulate the LLM outputting garbage that breaks the Pydantic parser
    mock_invoke = mocker.patch(
        "langchain_core.runnables.base.RunnableSequence.invoke"
    )
    mock_invoke.side_effect = Exception("Failed to parse JSON")

    # Run the node
    result = pm_agent_node(mock_initial_state)

    # Validate the error state triggers correctly
    assert result["prd_json"] is None
    assert result["current_error"] == "Failed to parse JSON"
