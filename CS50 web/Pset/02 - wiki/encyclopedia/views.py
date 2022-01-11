from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages

import random
from markdown2 import Markdown

from . import util


class Entry_Form(forms.Form):
    """
    Creation of django form with a title and a content fields.
    Only used to create new entry.
    """
    title = forms.CharField(label="Title :")
    content = forms.CharField(label="Text :", widget=forms.Textarea(attrs={"style":"height:30vh; width:75%"}))
    
class Entry_Edit_Form(forms.Form):
    """
    Creation of django form with a title and a content fields.
    Only used to edit existing entry content as title wont be editable by user 
    to prevent creation of another entry.
    """
    title = forms.CharField(label="Title :", widget=forms.HiddenInput())
    content = forms.CharField(label="Text :", widget=forms.Textarea(attrs={"style":"height:40vh; width:75%"}))    
    

def index(request):
    """ 
    Return a list of all available entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, entry):
    """ 
    Convert and display markdown content of selected entry.
    """
    if util.get_entry(entry) is None:
        return render(request, "encyclopedia/no_entry.html", {
            "entry": entry
        })
    markdowner = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "entry" : markdowner.convert(util.get_entry(entry)),
        "title": entry
    })
    
def search(request):
    """
    Redirect user directly to the entry page if search matches 
    perfectily with an entry title.
    Otherwise, returns to a list of possible entries.
    """
    if request.method == "GET":
        query = request.GET.get('q')
        # If the query matches the name of an encyclopedia entry, 
        # the user should be redirected to that entry’s page.
        if not util.get_entry(query) is None:
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': query}))
        else:
            # displays a list of all encyclopedia entries 
            # that have the query as a substring
            list_of_entries = []
            for entry in util.list_entries():
            # agressive insentive way of making strings comparison
                if query.casefold() in entry.casefold():
                    list_of_entries.append(entry)
            # if nothing exist
            if len(list_of_entries) == 0:
                return render(request, "encyclopedia/no_entry.html", {
                    "entry": query
                })
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "searched_entries": list_of_entries
            })
    return HttpResponseRedirect(reverse("index"))

def new_page(request):
    """
    Allow user to create a page by redirecting to an empty form,
    fill it and save it.
    """
    if request.method == "POST":
        form = Entry_Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            content = form.cleaned_data["content"]
            # Save the entry if it does not already exist and redirect user to new entry
            if util.get_entry(title) is None:  
                # Content with encoding 'utf-8'               
                util.save_entry(title, bytes(content, 'utf8'))
                messages.success(request, f"Entry '{title}' has been added !")                
                return HttpResponseRedirect(reverse("entry", kwargs={"entry": title})) 
            # elif entry exist display an error message 
            messages.error(request, f"Entry '{title}' already exist !")          
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })        
    return render(request, "encyclopedia/new_page.html", {
        "form": Entry_Form()
    })

def edit_page(request, title): 
    """
    When user click on edit button, redirects to an editing form 
    already filled with the entry content.
    """ 
    if request.method == 'GET':
        page_content = util.get_entry(title)        
        return render(request, "encyclopedia/edit_page.html", {
            'edit_form': Entry_Edit_Form(initial={'content': page_content, 'title': title})            
        })
    return HttpResponseRedirect(reverse("index"))

def save_edited_page(request, title):
    """
    Allow user to save his edition 
    and redirect him to the entry page.
    """
    if request.method == "POST":
        form = Entry_Edit_Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]  
            # Content with encoding 'utf-8'       
            util.save_entry(title, bytes(content, 'utf8'))
            messages.success(request, f"Entry '{title}' has been edited.")
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
        messages.error(request, "Entry is not editable !")
        return render(request, "encyclopedia/edit_page.html", {
            "edit_form" : form        
        })
    return HttpResponseRedirect(reverse("index"))
    
def random_page(request):
    """
    Redirect to a random displayed entry.
    """
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': entry}))

def delete_page(request, title):
    """
    Allow to delete an entry. (for convenient purpose)
    """
    if request.method == "GET":
        util.delete_entry(title)
        messages.error(request, f"Entry '{title}' has been deleted.")
        return redirect("index")
    return HttpResponseRedirect(reverse("index"))