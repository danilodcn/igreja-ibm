from igreja.apps.core.types.pages import Breadcrumb, PageLink

def web_context(request):
    breadcrumb = Breadcrumb(
        title="Dashboard",
        href="/meu",
        links=[
                PageLink(href="/", title="home"),
                PageLink(title="dashboard"),
            ]
        )

    return {
        "site_config": {
            "title": "IBM - Igreja Batista Missionária"
        },
        "page_config": {
            "breadcrumb": breadcrumb,
        }
    }