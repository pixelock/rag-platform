# coding: utf-8

import os
import glob
from datasets import load_dataset
from itertools import chain
from langchain.document_loaders import TextLoader

from utils.path import DOCS_DIR
from utils.log import logger


def load_documents(docs_dir, verbose=False):
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


class QAManager(object):
    def __init__(self, path):
        self.datasets = load_dataset('csv', data_files=path)

    def __len__(self):
        return len(self.datasets)
