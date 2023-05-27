from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from . import util
import random as rnd

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, entry):
    markdown_text=util.get_entry(entry)
    if markdown_text:
        context = {
            'entry_title' : entry,
            'entry' : util.markdown_to_html(markdown_text)
        }                  
        return render(request, "encyclopedia/entry.html", context)
    else: return render(request, "encyclopedia/404.html", status=404)
    
def search(request):
    query = request.GET.get('q', '')
    if util.get_entry(query):
        return redirect(entry, query)
    else:
        context={
            'matches': util.search_entries(query),
            'query': query,
        }
        return render(request, "encyclopedia/search.html", context)

def add(request):
    if request.method == "POST":
        form = util.NewPage(request.POST)
        if form.is_valid():  
            title= form.cleaned_data["title"]
            content= form.cleaned_data["content"]
            if title in util.list_entries():
                messages.info(request, f'{title} is already in encyclopedia!')
                return redirect('add')
            util.save_entry(title, f'# {title}\n\n{content}')
            return redirect("add")
    else:
        return render(request, "encyclopedia/add.html",{'form': util.NewPage() })

def edit(request, title):
    if request.method == 'POST':
        form = util.EditEntryForm(request.POST)
        if form.is_valid():
            modified_entry = form.cleaned_data['content']
            util.save_entry(title, modified_entry)
            context={
                'entry_title': title,
                'entry': util.markdown_to_html(modified_entry)
            }
            return render(request, "encyclopedia/entry.html", context)
    else:
        entry_content = util.get_entry(title)
        context={
            "title":title,
            "form":util.EditEntryForm(initial={'content': entry_content})
        }
        return render(request, "encyclopedia/edit.html", context)
    
def random(request):
    entry=rnd.choice(util.list_entries())
    return redirect('entry', entry)