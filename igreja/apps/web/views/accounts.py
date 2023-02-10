from django.views.generic.edit import CreateView
from django import forms
from igreja.apps.account.models import CustomUser


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = []


class CreateUserView(CreateView):
    template_name = "web/pages/accounts/create.html"
    success_url = "/"
    form_class = CustomUserForm

    def form_valid(self, form):
        import ipdb; ipdb.set_trace()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        import ipdb; ipdb.set_trace()
        ...