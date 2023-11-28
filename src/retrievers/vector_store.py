# coding: utf-8

from typing import Optional
from langchain.vectorstores.base import VectorStore
from langchain.vectorstores.base import VectorStoreRetriever

from retrievers.base import add_name


def vector_store_retriever_factory(
        *,
        vectorstore: VectorStore,
        retriever_name: Optional[str] = None
) -> VectorStoreRetriever:
    retriever = vectorstore.as_retriever()
    add_name(retriever, 'vectorstore', param_text=retriever_name)
    return retriever
