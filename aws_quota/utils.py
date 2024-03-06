import functools
import boto3
import traceback


@functools.lru_cache()
def get_account_id(session: boto3.Session) -> str:
    return session.client('sts').get_caller_identity()['Account']

def short_exception(exception: Exception) -> str:
    """
    Provides exception in a short format without traceback, example:
    >>> short_exception(BaseException("important error message"))
    'BaseException: important error message'
    """
    return ''.join(traceback.format_exception_only(type(exception), exception)).rstrip()


def get_paginated_results(session: boto3.Session, service: str, method: str, key: str, paginate_args: dict = {}) -> int:
    paginator = session.client(service).get_paginator(method)
    res = []
    for page in paginator.paginate(**paginate_args):
        res.extend(page[key])
    return res