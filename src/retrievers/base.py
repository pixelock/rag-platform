# coding: utf-8

from langchain.schema import BaseRetriever


class RetrieverMixin(object):
    @property
    def name(self):
        return self.metadata.get('name', None)

    @name.setter
    def name(self, retriever_name: str):
        self.metadata['name'] = retriever_name


def add_name(retriever: BaseRetriever, name: str, param_text: str = None):
    if param_text:
        final_name = name + f'({param_text})'
    else:
        final_name = name
    retriever.metadata['name'] = final_name


def get_name(retriever: BaseRetriever):
    return retriever.metadata.get('name', None)
