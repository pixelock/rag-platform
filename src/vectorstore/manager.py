# coding: utf-8

import os
from typing import Optional, List, Dict
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.utils import DistanceStrategy
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores.chroma import Chroma
from langchain.vectorstores.milvus import Milvus
from langchain.embeddings.base import Embeddings

from utils.path import DB_DIR


class VectorStoreManager(object):
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings

        self.collections = dict()

    def make_collection(
            self,
            collection_name: str,
            vectorstore_model: str = 'chroma',
            embeddings: Optional[Embeddings] = None,
            drop_old: bool = False,
            faiss_kwargs: Optional[Dict] = None,
            chroma_kwargs: Optional[Dict] = None,
            milvus_kwargs: Optional[Dict] = None,
    ):
        embeddings = embeddings or self.embeddings

        if vectorstore_model == 'chroma':
            persist_directory = os.path.join(os.path.join(DB_DIR, '.chroma'), collection_name)
            vector_store = self.make_chroma_vectorstore(
                embeddings=embeddings,
                collection_name=collection_name,
                persist_directory=persist_directory,
                drop_old=drop_old,
                **chroma_kwargs
            )
        elif vectorstore_model == 'milvus':
            vector_store = self.make_milvus_vectorstore(
                embeddings=embeddings,
                collection_name=collection_name,
                drop_old=drop_old,
                **milvus_kwargs
            )
        elif vectorstore_model == 'faiss':
            embedding_dim = faiss_kwargs.pop('embedding_dim')
            vector_store = self.make_faiss_vectorstore(
                embeddings=embeddings,
                embedding_dim=embedding_dim,
                **faiss_kwargs
            )
        else:
            raise ValueError(f'{vectorstore_model} vector store is not supported')
        self.collections[collection_name] = vector_store
        return vector_store

    @staticmethod
    def make_chroma_vectorstore(
            embeddings: Embeddings,
            collection_name: str,
            persist_directory: Optional[str] = None,
            drop_old: bool = False,
            server: bool = False,
            host: Optional[str] = 'localhost',
            port: Optional[str] = '8000',
            **kwargs
    ):
        import chromadb
        from chromadb.config import Settings

        if server:
            allow_reset = drop_old
            client = chromadb.HttpClient(host=host, port=port, settings=Settings(allow_reset=allow_reset))
            if allow_reset:
                client.reset()  # resets the database
        elif drop_old:
            client = chromadb.EphemeralClient()
        else:
            client = chromadb.PersistentClient(path=persist_directory)

        vectorstore = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_directory,
            **kwargs
        )

        return vectorstore

    @staticmethod
    def make_milvus_vectorstore(
            embeddings: Embeddings,
            collection_name: str,
            drop_old: bool = False,
            host: Optional[str] = '127.0.0.1',
            port: Optional[str] = '19530',
            **kwargs
    ):
        vector_store = Milvus(
            embedding_function=embeddings,
            collection_name=collection_name,
            connection_args={'host': host, 'port': port},
            drop_old=drop_old,
            **kwargs
        )

        return vector_store

    @staticmethod
    def make_faiss_vectorstore(
            embeddings: Embeddings,
            embedding_dim: int,
            normalize_l2: bool = False,
            distance_strategy: DistanceStrategy = DistanceStrategy.EUCLIDEAN_DISTANCE,
            **kwargs
    ):
        import faiss

        if distance_strategy == DistanceStrategy.MAX_INNER_PRODUCT:
            index = faiss.IndexFlatIP(embedding_dim)
        else:
            # Default to L2, currently other metric types not initialized.
            index = faiss.IndexFlatL2(embedding_dim)

        vectorstore = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
            normalize_L2=normalize_l2,
            **kwargs,
        )

        return vectorstore

    def get_collection(self, collection_name: str):
        return self.collections[collection_name]
