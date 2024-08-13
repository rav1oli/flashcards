from django import template
import markdown
from urllib.parse import urlencode

register = template.Library()

@register.filter
def index(list, i):
    return list[i]

@register.filter
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text, safe_mode='escape') 

@register.filter
def urlencoderight(request_data):
    copy = dict(request_data.lists())
    return urlencode(copy, doseq=True)