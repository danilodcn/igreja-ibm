from typing import Dict
from django.http.response import HttpResponse


def get_redirect(query_params: Dict[str, str]):
    next = query_params.get("next", None)

    if next and isinstance(next, str):
        if "/" not in next:
            return
        _, *resources = next.split("/")
        return"/".join(resources)

    return "/"