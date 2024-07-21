from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import *

# Create your views here.
class CardList(ListView):
    model = Card

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        if user.is_authenticated:
            return Card.objects.filter(user=user)
        else:
            return Card.objects.none
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "frontend/partials/cards.html"
        else:
            template_name = "frontend/card-list.html"
        return [template_name]


