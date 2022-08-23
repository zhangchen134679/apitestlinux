import requests
from common.handler_logging import logger

logger = logger()


def visit(url=None, method=None, params=None, data=None, json=None, **kwargs):
    """
    调用visit函数时,使用方法为 :
    visit(url, method, json, headers)
    lower()全部转化为小写
    """
    method = method.lower()

    res = requests.request(url=url, method=method, params=params, data=data, json=json, **kwargs)
    try:
        if isinstance(res.json(), dict):
            res.json = res.json()
            return res.json
    except Exception as err:
        logger.error(f"RequestsError..{url}")
        logger.error(f"RequestsError..{res}..")
        logger.error(f"RequestsError..{res.text}")
        raise err
































