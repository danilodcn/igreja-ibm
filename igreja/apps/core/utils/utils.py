from typing import Any, List, Tuple
from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse


def get_filename(filename: str) -> str:
    return filename.lower()


def get_admin_url(obj):
    return reverse(
        "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
        args=[obj.id],
    )


def get_field_display(
    choices: List[Tuple[int | str], Any],
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
