from typing import Type

from crispy_forms.utils import render_crispy_form
from django import forms
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
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


class AjaxView(View):
    form_class: Type[forms.Form]
    status_success = 200
    status_error = 400

    def get_object(self, *args, **kwargs):
        raise NotImplementedError()

    def get_form(self, *args, **kwargs):
        data = dict(
            data=self.request.POST,
            files=self.request.FILES,
        )
        data.update(kwargs)
        print(data)

        return self.form_class(**data)

    def form_valid(self) -> forms.Form:
        form = self.get_form(instance=self.get_object())
        form.save()
        return form

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.get_form()
        is_valid = form.is_valid()
        if is_valid:
            form = self.form_valid()
            status = self.status_success
        else:
            status = self.status_error

        form_rendered = render_crispy_form(
            form, context={"initial": self.request.POST}
        )

        return JsonResponse(
            {"success": is_valid, "errors": form.errors, "form": form_rendered},
            status=status,
        )

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        form_rendered = render_crispy_form(form, context={})
        return JsonResponse(
            {"success": True, "form": form_rendered},
            status=self.status_success,
        )
