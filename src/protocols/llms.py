# coding: utf-8

from protocols.base import StrEnum


class LLM(StrEnum):
    GPT_35_TURBO = 'gpt_35_turbo'
    GPT_35_TURBO_16K = 'gpt_35_turbo_16k'


LLMMaxToken = {
    LLM.GPT_35_TURBO: 4096,
    LLM.GPT_35_TURBO_16K: 16384,
}
