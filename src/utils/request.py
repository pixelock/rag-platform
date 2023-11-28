# coding: utf-8

import time
import requests

from utils.log import logger


def safe_retry_request(url, data=None, json_=None, headers=None, timeout=60, retry=3, retry_delta=5, verbose=False):
    tic = time.time()
    assert isinstance(retry, int) and retry >= 1

    for i in range(retry):
        try:
            resp = requests.post(url=url, data=data, json=json_, headers=headers, timeout=timeout)
            if verbose:
                logger.info(f'code: {resp.status_code}')

            resp_json = resp.json()
            if verbose:
                logger.info(f'request {url} cost {(time.time() - tic) * 1000}ms')

            return resp_json
        except Exception as e:
            if i + 1 < retry:
                if verbose:
                    try:
                        logger.info(f'{resp.text} occurred while requesting [{url}], retry {i + 1} time, suspending {retry_delta ** (i + 1)}s')
                    except Exception as _:
                        logger.info(f'{type(e)} occurred while requesting [{url}], retry {i + 1} time, suspending {retry_delta ** (i + 1)}s')

                time.sleep(retry_delta ** (i + 1))
            else:
                raise e

    if verbose:
        logger.info(f'request {url} cost {(time.time() - tic) * 1000}ms')

    return None
