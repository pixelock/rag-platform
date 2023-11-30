# coding: utf-8

from typing import Any, Callable
from langchain.text_splitter import RecursiveCharacterTextSplitter

from splitters.base import TextSplitterMixin


class RecursiveChineseTextSplitter(RecursiveCharacterTextSplitter, TextSplitterMixin):
    def __init__(
            self,
            chunk_size: int,
            chunk_overlap: int,
            length_function: Callable[[str], int] = len,
            keep_separator: bool = True,
            is_separator_regex: bool = False,
            **kwargs: Any
    ):
        super(RecursiveChineseTextSplitter, self).__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function,
            keep_separator=keep_separator,
            is_separator_regex=is_separator_regex,
            separators=['\n\n', '\n', '。', '！', '？', '；', '，'],
            **kwargs,
        )
        self.name = f'recursive-chinese(chunk_size={chunk_size},chunk_overlap={chunk_overlap})'
