from typing import Dict

from pydantic import BaseModel, Field


class CodeArtifacts(BaseModel):
    files: Dict[str, str] = Field(
        ...,
        description=(
            "A dictionary where the keys are the exact filepaths "
            "and the values are the raw code strings."
        ),
    )
