# coding: utf-8

from typing import List, cast
from langchain.embeddings import CacheBackedEmbeddings as LangchainCached


class CacheBackedEmbeddings(LangchainCached):
    def embed_query(self, text: str) -> List[float]:
        vector = self.document_embedding_store.mget([text])[0]
        is_missing = bool(vector is None)
        if is_missing:
            vector = self.underlying_embeddings.embed_query(text)
            self.document_embedding_store.mset([(text, vector)])

        return cast(List[float], vector)

    @property
    def name(self):
        return self.underlying_embeddings.name
