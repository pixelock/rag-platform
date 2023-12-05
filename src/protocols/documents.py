# coding: utf-8

from pydantic import BaseModel
from typing import Optional


class DocumentMetadata(BaseModel):
    doc_id: str
    source: str
    source_name: str
    chunk_id: str
    chunk_index: int = 0
    chunk_level: int = 0
    parent_id: Optional[str] = None
