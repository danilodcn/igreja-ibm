from typing import Dict
from urllib import parse
from django.http.response import HttpResponse


def get_redirect(query_params: Dict[str, str]):
    next = query_params.get("next", None)
    if next:
        parsed = parse.urlparse(next)
        return '{uri.path}?{uri.query}'.format(uri=parsed)
    return None
