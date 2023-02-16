from django.shortcuts import render

# Create your views here.


def home(request, slug=None):
    ctx = {}
    ctx["selected_church"] = {"slug": slug}
    return render(request, "web/index.html", context=ctx)
