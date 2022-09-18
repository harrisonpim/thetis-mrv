from pydantic import BaseModel
from fastapi import responses
import orjson
from typing import Any, List
from src import Entry


class ORJSONResponse(responses.JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


class EntriesResponse(BaseModel):
    nextPage: str
    entries: List[Entry]
