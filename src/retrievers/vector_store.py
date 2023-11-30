# coding: utf-8

from typing import List, Dict, Optional
from langchain.schema import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.text_splitter import TextSplitter
from vectorstore.manager import VectorStoreManager

from retrievers.base import add_name


def vector_store_retriever_factory(
        *,
        documents: List[Document],
        embeddings: Embeddings,
        text_splitter: TextSplitter,
        vectorstore_manager: VectorStoreManager,
        vectorstore_model: str = 'chroma',
        vectorstore_kwargs: Optional[Dict] = None
) -> VectorStoreRetriever:
    vectorstore_kwargs = vectorstore_kwargs or {}
    sub_docs = text_splitter.split_documents(documents)
    collection_name = f'vector-{embeddings.name}-{text_splitter.id}'
    vectorstore = vectorstore_manager.make_collection(
        collection_name=collection_name,
        vectorstore_model=vectorstore_model,
        embeddings=embeddings,
        drop_old=True,
        **vectorstore_kwargs
    )
    vectorstore.add_documents(sub_docs)
    retriever = vectorstore.as_retriever()
    add_name(retriever, f'{embeddings.name}-vector', param_text=text_splitter.name)
    return retriever
