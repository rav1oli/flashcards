
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import *

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    

class CardList(ListView):
    model = Card

    def get_queryset(self):

        order_by = self.request.GET.get('order_by', 'date_created')
        tag_id = int(self.request.GET.get('filter', 0))

        user = self.request.user
        if user.is_authenticated:
            user_cards = Card.objects.filter(user=user)
            if tag_id == 0:
                return user_cards.order_by(order_by)
            else:
                return user_cards.filter(tags__id=tag_id).order_by(order_by)
        else:
            return Card.objects.none
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "frontend/partials/cards.html"
        else:
            template_name = "frontend/card-list.html"
        return [template_name]

def tag_list(request):
    return render(request, 'frontend/partials/tags.html', {
        'tag_list': Tag.objects.all()
    })
