# coding: utf-8

from pydantic import BaseModel
from typing import List, Optional, Union


class EmbeddingRequest(BaseModel):
    input: Union[str, List[int], List[str], List[List[int]]]
    model: Optional[str]
    object: str = 'embedding'


class EmbeddingData(BaseModel):
    index: int
    embedding: Union[List[float], List[List[float]]]
    object: str = 'embedding'


class EmbeddingUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class EmbeddingResponse(BaseModel):
    data: List[EmbeddingData]
    model: Optional[str] = None
    object: Optional[str] = None
    usage: Optional[EmbeddingUsage] = None
