from typing import Dict
from urllib import parse

from django.http.response import HttpResponse


def get_redirect(query_params: Dict[str, str]) -> str:
    """
    Usa o atributo `next` passado na query string para construir em um nova query string

    Examples:
        >>> get_redirect({'next': 'https://xpto/path?a=3&b=7'})
        '/path?a=3&b=7'
    """
    next = query_params.get("next", None)
    if next:
        parsed = parse.urlparse(next)
        return "{uri.path}?{uri.query}".format(uri=parsed)
    return None
