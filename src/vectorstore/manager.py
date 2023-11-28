# coding: utf-8

import os
from typing import Optional, List
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import TextSplitter

from utils.path import DB_DIR


class VectorStoreManager(object):
    def __init__(self, embeddings: Embeddings, vectorstore_model: str = 'chroma', text_splitter: Optional[TextSplitter] = None):
        self.embeddings = embeddings
        self.vectorstore_model = vectorstore_model
        if vectorstore_model == 'chroma':
            self.model = Chroma
        elif vectorstore_model == 'faiss':
            self.model = FAISS
        else:
            raise ValueError(f'{vectorstore_model} vector store is not supported')
        self.text_splitter = text_splitter

        self.collections = dict()

    def make_collection(
            self,
            collection_name: str,
            docs: List[Document],
            embeddings: Optional[Embeddings] = None,
            text_splitter: Optional[TextSplitter] = None,
            persist_directory: Optional[str] = os.path.join(DB_DIR, '.chroma'),
            **kwargs
    ):
        embeddings = embeddings or self.embeddings
        text_splitter = text_splitter or self.text_splitter

        texts = text_splitter.split_documents(docs)
        if self.vectorstore_model == 'chroma':
            kwargs.update({
                'collection_name': collection_name,
                'persist_directory': os.path.join(persist_directory, collection_name),
            })
        vector_store = self.model.from_documents(documents=texts, embedding=embeddings, **kwargs)
        self.collections[collection_name] = vector_store
        return vector_store

    def get_collection(self, collection_name: str):
        return self.collections[collection_name]
