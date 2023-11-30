# coding: utf-8

from typing import List, Union
from langchain.embeddings.base import Embeddings

from utils.request import safe_retry_request
from protocols.embeddings import EmbeddingRequest, EmbeddingResponse


class RemoteEmbeddings(Embeddings):
    def __init__(self, url: str, model: str = 'bge', headers: dict = None, retry: int = 3, retry_delta: int = 5, verbose: bool = False):
        self.url = url
        self.model = model
        self.headers = headers
        self.retry = retry
        self.retry_delta = retry_delta
        self.verbose = verbose

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.get_embeddings(text=texts)

    def embed_query(self, text: str) -> List[float]:
        return self.get_embeddings(text=text)

    def get_embeddings(self, text: Union[str, List[str]]):
        request = EmbeddingRequest(input=text, model=self.model)
        body = request.model_dump(mode='json')
        resp = safe_retry_request(
            url=self.url,
            json_=body,
            headers=self.headers,
            retry=self.retry,
            retry_delta=self.retry_delta,
            verbose=self.verbose,
        )
        resp_struct = EmbeddingResponse(**resp)
        if isinstance(text, str):
            vectors = resp_struct.data[0].embedding
        else:
            vectors = [data.embedding for data in resp_struct.data]

        return vectors

    def name(self):
        return self.model
