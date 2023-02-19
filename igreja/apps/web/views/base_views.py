from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.edit import FormView

from igreja.apps.core.utils.redirect import get_redirect


class FormBaseView(FormView):
    def form_invalid(self, form) -> HttpResponse:
        for errors in form.errors.values():
            for msg in errors:
                messages.error(self.request, msg)
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        url = get_redirect(self.request.GET)
        if url:
            return url
        return super().get_success_url()
