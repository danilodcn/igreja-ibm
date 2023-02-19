from urllib.parse import urlencode

from django.utils.deprecation import MiddlewareMixin

from igreja.apps.core.utils.redirect import get_redirect


class QueryStringMiddleware(MiddlewareMixin):
    def process_request(self, request):
        data = request.GET.copy()
        next = data.get("next")
        if next:
            url = get_redirect(data)
            data["next"] = url

        request.query_string = urlencode(data)
