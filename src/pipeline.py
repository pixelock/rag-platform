# coding: utf-8

import os
import argparse
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache

from utils.log import logger
from utils.path import QA_DIR, DOCS_DIR, CACHE_DIR
from utils.load import load_documents, QAManager
from embeddings.remote import RemoteEmbeddings
from splitters.recursive import RecursiveChineseTextSplitter
from vectorstore.manager import VectorStoreManager
from retrievers.vector_store import vector_store_retriever_factory


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default='test', help='name of the pipeline')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='LLM model name')
    parser.add_argument('--embedding', type=str, default='ada', choices=['ada', 'bge'], help='embedding model name')
    parser.add_argument('--temperature', type=float, default=0.5, help='temperature of LLM generating process')
    parser.add_argument('--qa', type=str, default='qa.csv', help='file name of query-answer pairs dataset')
    parser.add_argument('--docs', type=str, default='docs', help='directory name of document files')
    parser.add_argument('--use_cache', action='store_true', help='whether to use LLM cache')
    parser.add_argument('--verbose', action='store_true', help='whether to print runtime details')
    args = parser.parse_args()

    logger.info(f'LLM: {args.model}')
    logger.info(f'embedding model: {args.embedding}')
    logger.info(f'pipeline name: {args.name}')
    logger.info(f'temperature: {args.temperature}')

    qa_path = os.path.join(QA_DIR, args.qa)
    docs_dir = os.path.join(DOCS_DIR, args.docs)
    logger.info(f'query-answer pairs dataset file: {qa_path}')
    logger.info(f'document files directory: {docs_dir}')

    # load QA pairs dataset
    qa_manager = QAManager(qa_path)
    logger.info(f'number of query-answer pairs: {len(qa_manager)}')

    # load documents
    documents = load_documents(docs_dir, verbose=args.verbose)
    logger.info(f'number of total documents: {len(documents)}')

    # initialize embedding system
    fs = LocalFileStore(os.path.join(CACHE_DIR, args.embedding))
    embeddings = RemoteEmbeddings(
        url=os.environ.get('EMBEDDING_URL'),
        model=args.embedding,
        headers={'Authorization': os.environ.get('EMBEDDING_AUTH')},
        verbose=args.verbose,
    )
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=embeddings,
        document_embedding_cache=fs,
        namespace=args.embedding,
    )

    # build different text splitter
    splitter_rec_100 = RecursiveChineseTextSplitter(chunk_size=100, chunk_overlap=100)
    splitter_rec_200 = RecursiveChineseTextSplitter(chunk_size=200, chunk_overlap=100)
    splitter_rec_400 = RecursiveChineseTextSplitter(chunk_size=400, chunk_overlap=100)

    vector_store_manager = VectorStoreManager(embeddings=cached_embeddings)


    vector_store_retriever_factory(documents=documents, vectorstore_manager=vector_store_manager)


