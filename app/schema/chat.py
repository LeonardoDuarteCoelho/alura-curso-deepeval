from pydantic import BaseModel, Field
from typing import List, Dict, Any, Annotated

class ChatRequest(BaseModel):
    question: str
    history: List[Dict[str, Any]] = []
    model: Annotated[str | None, Field(
        default=None,
        description="Opcional. Identificador do modelo no LM Studio; se omitido, usa LM_STUDIO_MODEL do arquivo .env.",
    )]
