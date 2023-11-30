# coding: utf-8

import hashlib


def text_hash(text):
    hash_obj = hashlib.md5(string=text.encode('utf-8'))
    hash_value = hash_obj.hexdigest()
    return hash_value
