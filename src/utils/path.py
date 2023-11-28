# coding: utf-8

import os

ROOT_DIR = os.path.abspath(
    os.path.join(  # rag-platform
        os.path.join(  # rag-platform/src
            os.path.dirname(__file__),
            '..'
        ),
        '..'
    )
)

LOG_DIR = os.path.join(ROOT_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

CACHE_DIR = os.path.join(ROOT_DIR, 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

DB_DIR = os.path.join(ROOT_DIR, 'db')
os.makedirs(DB_DIR, exist_ok=True)

RESOURCES_DIR = os.path.join(ROOT_DIR, 'resources')
os.makedirs(RESOURCES_DIR, exist_ok=True)
DOCS_DIR = os.path.join(RESOURCES_DIR, 'docs')
os.makedirs(DOCS_DIR, exist_ok=True)
QA_DIR = os.path.join(RESOURCES_DIR, 'qas')
os.makedirs(QA_DIR, exist_ok=True)
