from operator import add
from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import BaseMessage

# Import our Pydantic schemas (we will build these next)
from tri_loop_dev.schemas.prd import PRDSchema
from tri_loop_dev.schemas.system import SystemArchitectureSchema


class AgentState(TypedDict):
    """
    The shared state for the tri-loop-dev multi-agent workflow.
    Each field acts as a persistent memory slot for the graph.
    """

    # The conversation log, appended to by all agents
    messages: Annotated[List[BaseMessage], add]

    # Validated artifacts passed between personas
    prd_json: Optional[PRDSchema]
    architecture_schema: Optional[SystemArchitectureSchema]

    # Execution artifacts
    code_artifacts: Optional[dict]

    # Error state for the self-correction loop
    current_error: Optional[str]

    # Metadata for cost/step management
    is_approved: bool  # Used by the Human-in-the-Loop (HITL) checkpoint
