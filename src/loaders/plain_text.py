# coding: utf-8

import os
import glob
from itertools import chain
from langchain.document_loaders import TextLoader

from utils.log import logger
from utils.path import DOCS_DIR
from utils.text import text_hash
from protocols.documents import DocumentMetadata


class PlainTextDocumentLoader(object):
    def __init__(self, doc_dataset_name: str, verbose: bool = False):
        self.verbose = verbose

        self.documents = []
        self.mapping = dict()
        self.load_documents(path=os.path.join(DOCS_DIR, doc_dataset_name))

    def load_documents(self, path):
        doc_file_paths = [name for name in chain(glob.glob(f'{path}/*.md'), glob.glob(f'{path}/*.txt'))]

        if self.verbose:
            logger.info(f'loading {len(doc_file_paths)} document files from {path}')

        for path in doc_file_paths:
            self.load(path)

        if self.verbose:
            logger.info(f'total documents number: {len(self.documents)}')

    def load(self, path: str):
        doc_loader = TextLoader(path)
        raw_documents = doc_loader.load()
        for i, doc in enumerate(raw_documents):
            doc_id = text_hash(doc.page_content)
            meta_data = DocumentMetadata(
                doc_id=doc_id,
                source=doc.metadata['source'],
                source_name=os.path.split(path)[1],
                chunk_id=doc_id,
                chunk_index=i,
            ).model_dump(mode='json')
            doc.metadata = meta_data

            if doc_id in self.mapping:
                continue
            self.documents.append(doc)
            self.mapping[doc_id] = doc

        if self.verbose:
            logger.info(f'{len(raw_documents)} document(s) have successfully been loaded from {path}')

    def get_document(self, doc_id: str):
        return self.documents[doc_id]

    def __len__(self):
        return len(self.documents)

    def __getitem__(self, item: str):
        return self.get_document(item)
