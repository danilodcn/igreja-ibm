from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from crispy_forms.utils import render_crispy_form
from django import forms
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View


class AjaxFormMixin:
    def __init__(self, request, *args, validate_form: bool=True, **kwargs):
        super().__init__(*args, **kwargs)

        if not validate_form:
            for key in self.fields:
                self.fields[key].required = False

        self.validate_form = validate_form
        self.request = request

    def _clean_fields(self):
        for name, bf in self._bound_items():
            field = bf.field
            value = bf.initial if field.disabled else bf.data
            try:
                if isinstance(field, forms.FileField):
                    value = field.clean(value, bf.initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if self.validate_form and hasattr(self, "clean_%s" % name):
                    value = getattr(self, "clean_%s" % name)()
                    self.cleaned_data[name] = value
            except forms.ValidationError as e:
                self.add_error(name, e)


class AjaxViewMixin(ABC):
    form_class: Type[forms.Form]
    status_success = 200
    status_error = 400

    @abstractmethod
    def form_is_valid(self, form: forms.Form) -> Any:
        raise NotImplementedError

    def get_form_kwargs(self, **kwargs) -> Dict[str, Any]:
        kwargs["data"] = self.request.POST
        kwargs["files"] = self.request.FILES
        kwargs["request"] = self.request
        return kwargs
    
    def get_form(self, **kwargs):
        data = self.get_form_kwargs(**kwargs)
        return self.form_class(**data)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = self.get_form(validate_form=True)
        is_valid = form.is_valid()
        if is_valid:
            self.form_is_valid(form)
            status = self.status_success
        else:
            status = self.status_error

        form_rendered = render_crispy_form(
            form, context={"initial": self.request.POST}
        )   

        return JsonResponse(
            {"success": is_valid, "errors": form.errors, "form": form_rendered, 'fields': form.data},
            status=status,
        )


    def get(self, request: HttpRequest, *args, **kwargs):
        form = self.get_form(validate_form=False)

        form_rendered = render_crispy_form(form, context={})
        return JsonResponse(
            {"success": True, "form": form_rendered, 'fields': form.data},
            status=self.status_success,
        )


class AjaxView(View, AjaxViewMixin):
    def form_is_valid(form):
        raise NotImplementedError