# coding: utf-8

from enum import Enum


class StrEnum(Enum):
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value.replace('_', '').lower() == value.replace('-', '').replace('_', '').lower():
                return member
