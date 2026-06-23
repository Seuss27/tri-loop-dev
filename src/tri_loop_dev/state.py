from operator import add
from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import BaseMessage

from tri_loop_dev.schemas.architect import ArchitectureSchema

# Import our Pydantic schemas
from tri_loop_dev.schemas.prd import PRDSchema


class AgentState(TypedDict):
    """
    The shared state for the tri-loop-dev multi-agent workflow.
    Each field acts as a persistent memory slot for the graph.
    """

    # The conversation log, appended to by all agents
    messages: Annotated[List[BaseMessage], add]

    # Validated artifacts passed between personas
    prd_json: Optional[PRDSchema]

    # Updated to use the strict ArchitectureSchema
    architecture_schema: Optional[ArchitectureSchema]

    # Execution artifacts
    code_artifacts: Optional[dict]

    # Error state for the self-correction loop
    current_error: Optional[str]

    # Metadata for cost/step management
    is_approved: bool  # Used by the Human-in-the-Loop (HITL) checkpoint

    # Retry count for self-correction loop
    retry_count: int = 0
