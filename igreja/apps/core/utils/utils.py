import secrets
from os.path import splitext
from typing import Any, List, Tuple
from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse


def get_filename(filename: str) -> str:
    """
    Cria um novo nome de aquivo aleatório usando um hash de 8 dígitos concatenado com o nome do arquivo.

    Examples:
        >>> new_name = get_filename("file.png")
        >>> type(new_name)
        <class 'str'>
        >>> "file" in new_name
        True
        >>> ".png" in new_name
        True

    """
    hash = secrets.token_urlsafe(8)
    name, ext = splitext(filename.lower())
    return f"{name}-{hash}{ext}"


def get_admin_url(obj):
    return reverse(
        "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
        args=[obj.id],
    )


def get_field_display(
    choices: Tuple[List[int | str], Any],
    value: int | str,
    raise_exception=False,
):
    for i, choice in choices:
        if i == value:
            return choice

    if raise_exception:
        raise ValueError(f"'{value}' not found in {choices}")


def build_site_uri(url: str):
    site_url = settings.SITE_ABSOLUTE_URL
    return urljoin(site_url, url)
