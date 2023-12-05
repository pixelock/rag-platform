# coding: utf-8

from abc import ABC, abstractmethod


class EmbeddingMixin(ABC):
    @property
    @abstractmethod
    def name(self):
        """Name of embedding model"""
