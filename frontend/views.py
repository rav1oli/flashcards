
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django_htmx.http import HttpResponseClientRedirect

from .models import *
from .forms import *

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class IndexView(TemplateView):
    template_name = "frontend/index.html"


class CardListTemplateView(TemplateView):
    template_name = "frontend/card-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_list'] = Card.objects.filter(user=self.request.user)
        return context


class CardListView(ListView):
    model = Card
    template_name = "frontend/partials/cards.html"

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


class TagSelectView(ListView):
    template_name = "frontend/partials/tag-select.html"

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)
    

def tag_card_form(request, pk):
    card = Card.objects.get(pk=pk)

    if request.method == "POST":
        form = TagCheckboxForm(request.POST, context={'user': request.user}, instance=card)
        if form.is_valid():
            form.save()
            return 
        else: 
            return HttpResponseClientRedirect(reverse('cards'))
    else: 
        form = TagCheckboxForm(context={'user': request.user}, instance=card)
        return render(request, 'frontend/partials/tag-card-form.html', {'form': form})


def delete_card(request, pk):
    if request.method == "DELETE":
        Card.objects.get(pk=pk).delete()

        return HttpResponseClientRedirect(reverse('card_list'))