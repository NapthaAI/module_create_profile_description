from typing import Optional, List
from pydantic import BaseModel


class InputSchema(BaseModel):
    points: List[str]
    output: Optional[str] = None