# coding: utf-8

from enum import Enum
from langchain.prompts import PromptTemplate as LangchainPromptTemplate


class Task(str, Enum):
    RAG = 'rag'
    DETERMINE = 'determine'


class PromptTemplate(LangchainPromptTemplate):
    def __len__(self):
        return len(self.template)
