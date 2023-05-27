import re
import markdown2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django import forms

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    
def search_entries(query):
    results = []
    for entry in list_entries():
        if re.findall(query, entry, re.IGNORECASE):
            results.append(entry)
    return results

def markdown_to_html(markdown_text):
    html_text=markdown2.markdown(markdown_text)
    return html_text
    
class NewPage(forms.Form):

    title = forms.CharField(
        max_length=80,
        required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea)
    
class EditEntryForm(forms.Form):
    required=True
    content = forms.CharField(widget=forms.Textarea, label='')
