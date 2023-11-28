# coding: utf-8

import os
import glob
from itertools import chain
from langchain.document_loaders import TextLoader

from utils.path import DOCS_DIR
from utils.log import logger


def load_documents(file_dir='docs', verbose=False):
    docs_dir = os.path.join(DOCS_DIR, file_dir)
    doc_files = [
        os.path.join(docs_dir, file)
        for file in chain(
            glob.glob(f'{docs_dir}/*.md'),
            glob.glob(f'{docs_dir}/*.txt'),
        )
    ]
    if verbose:
        logger.info(f'loading document files from {docs_dir}')

    loaders = []
    for path in doc_files:
        loaders.append(TextLoader(path))
        if verbose:
            logger.info(f'document have successfully been loaded from {path}')

    docs = []
    for l in loaders:
        docs.extend(l.load())
    if verbose:
        logger.info(f'total documents number: {len(docs)}')

    return docs
