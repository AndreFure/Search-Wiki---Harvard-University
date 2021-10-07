import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import util
import random
from django.core.files.storage import default_storage
from django.urls import reverse

# Sidebar form (reformado)


class SearchForm(forms.Form):
    query = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'placeholder': 'Search Wiki', 'style': 'width:100%'}))

# Homepage (reformado)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

# New entry form. (reformado)


class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'placeholder': 'Enter new wiki title'}))
    data = forms.CharField(label="", widget=forms.Textarea())
# Edit entry form. (reformado)


class EditPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput())
    data = forms.CharField(label="", widget=forms.Textarea())
# Wiki/Error url (reformado)


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(util.get_entry(title)),
        "entry_raw": util.get_entry(title),
        "form": SearchForm()
    })
# Search entry


def search(request):
    if request.method == "POST":
        entries_found = []
        titles = util.list_entries()
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            for entry in titles:
                if query.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    return HttpResponseRedirect(reverse("entry", args=[title]))
                if query.lower() in entry.lower():
                    entries_found.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": entries_found,
                "query": query,
                "form": SearchForm()
            })
    return render(request, "encyclopedia/search.html", {
        "results": "",
        "query": "",
        "form": SearchForm()
    })


# Create new entry


def create(request):
    if request.method == "POST":
        newInformation = NewPageForm(request.POST)
        if newInformation.is_valid():
            title = newInformation.cleaned_data["title"]
            titles = util.list_entries()
            for entry in titles:
                if entry.lower() == newInformation.cleaned_data["title"].lower():
                    return render(request, "encyclopedia/create.html", {
                        "form": SearchForm(),
                        "newPageForm": NewPageForm(),
                        "error": "This wiki entry has been uploaded before."
                    })
            new_entry_title = "# " + newInformation.cleaned_data["title"]
            newInformation = "\n" + newInformation.cleaned_data["data"]
            new_entry_content = new_entry_title + newInformation
            util.save_entry(title, new_entry_content)
            entry = util.get_entry(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdown2.markdown(entry),
                "form": SearchForm()
            })
    return render(request, "encyclopedia/create.html", {
        "form": SearchForm(),
        "newPageForm": NewPageForm()
    })
# Edit entry (modificado)


def editEntry(request, title):
    if request.method == "POST":
        entry = util.get_entry(title)
        formModify = EditPageForm(initial={'title': title, 'data': entry})
        return render(request, "encyclopedia/edit.html", {
            "form": SearchForm(),
            "editPageForm": formModify,
            "entry": entry,
            "title": title
        })
# Submit entry edit (modificado)


def submitEditEntry(request, title):
    if request.method == "POST":
        modifyEntry = EditPageForm(request.POST)
        if modifyEntry.is_valid():
            entryEdit = modifyEntry.cleaned_data["title"]
            if entryEdit != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            util.save_entry(entryEdit, modifyEntry.cleaned_data["data"])
            entry = util.get_entry(entryEdit)
            msg_success = "You have been able to modify it."
        return render(request, "encyclopedia/entry.html", {
            "title": entryEdit,
            "entry": markdown2.markdown(entry),
            "form": SearchForm(),
            "msg_success": msg_success
        })

# Random entry (modificado)


def randomEntry(request):
    entry = util.get_entry(util.list_entries())
    return HttpResponseRedirect(reverse("entry", args=[random.choice(util.list_entries())]))
