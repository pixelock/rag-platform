# coding: utf-8

from utils.text import text_hash


class TextSplitterMixin(object):
    @property
    def chunk_size(self):
        return self._chunk_size if hasattr(self, '_chunk_size') else None

    @property
    def chunk_overlap(self):
        return self._chunk_overlap if hasattr(self, '_chunk_overlap') else None

    @property
    def separators(self):
        return self._separators if hasattr(self, '_separators') else None

    @property
    def separator(self):
        return self._separators if hasattr(self, '_separators') else None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def id(self):
        return text_hash(self._name)
