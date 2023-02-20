from igreja.apps.core.types.pages import Breadcrumb, PageLink

from .utils.redirect import get_redirect


def web_context(request):
    breadcrumb = Breadcrumb(
        title="Dashboard",
        href="/meu",
        links=[
            PageLink(href="/", title="home"),
            PageLink(title="dashboard"),
        ],
    )

    next = get_redirect(request.GET)

    request

    return {
        "url_next": next,
        "site_config": {"title": "IBM - Igreja Batista Missionária"},
        "page_config": {
            "breadcrumb": breadcrumb,
        },
    }
