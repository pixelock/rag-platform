# coding: utf-8

from enum import Enum


class EmbeddingModel(str, Enum):
    BGE = 'bge'
    ADA = 'ada'
    M3E = 'm3e'


EmbeddingDim = {
    EmbeddingModel.BGE: 1024,
    EmbeddingModel.ADA: 1536,
    EmbeddingModel.M3E: 768,
}
