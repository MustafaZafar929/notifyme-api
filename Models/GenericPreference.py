from pydantic import BaseModel
from typing import Dict , Any

class GenericPreference(BaseModel):
    table:str
    data: dict [str , Any]
    