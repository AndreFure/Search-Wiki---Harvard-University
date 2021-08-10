from django.shortcuts import render

from . import util

entries = {
    "css": "My css",
    "Django": "My Django",
    "HTML": "My HTML",
    "Python": "My Python"
}


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
