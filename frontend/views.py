
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import inlineformset_factory
from django_htmx.http import HttpResponseClientRedirect

from .models import *
from .forms import *
from .util import *

def get_filtered_and_sorted_user_cards(request, post=False):
    if post:
        order_by = request.POST.get('order_by', 'date_created')
        tag_id = int(request.POST.get('filter', 0))
    else:
        order_by = request.GET.get('order_by', 'date_created')
        tag_id = int(request.GET.get('filter', 0))
    

    card_list = get_user_cards(request.user)

    if tag_id == 0:
        return card_list.order_by(order_by)
    else:
        return card_list.filter(tags__id=tag_id).order_by(order_by)

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class IndexView(TemplateView):
    template_name = "frontend/index.html"


def card_list_view(request):

    if request.htmx:
        template_name = 'frontend/partials/cards.html'

        tag_id = int(request.GET.get('filter', 0))
        request.session['preselected_tag'] = tag_id

        order = request.GET.get('order_by', "date_created")
        request.session['preselected_order'] = order

    else:
        template_name = 'frontend/card-list.html'

    card_list = get_filtered_and_sorted_user_cards(request)

    return render(request, template_name, {'card_list': card_list})


def tag_select_list(request):
    preselected_tag = request.session.get('preselected_tag', 0)

    form = TagSelectForm(context={'user': request.user,}, initial={'tags': preselected_tag})

    return render(request, 'frontend/partials/tag-select-list.html', {
        'form': form,
    })
    

def order_select_list(request):
    preselected_order = request.session.get('preselected_order', "date_created")

    form = OrderSelectForm(initial={'order_by': preselected_order})

    return render(request, 'frontend/partials/order-select-list.html', {
        'form': form,
    })

def create_card_form(request):

    if request.method == "POST":
        form = CardForm(request.POST, context={'user': request.user})
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('create_card'))
        else: 
            return render(request, 'frontend/card-create-form.html', {'form': form})
    else: 
        form = CardForm(context={'user': request.user})
        return render(request, 'frontend/card-create-form.html', {'form': form})


def update_card_form(request, pk):
    card = Card.objects.get(pk=pk)

    if request.method == "POST":
        form = CardForm(request.POST, context={'user': request.user}, instance=card)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('card_list'))
        else: 
            return render(request, 'frontend/card-create-form.html', {'form': form})
    
    else:
        form = CardForm(context={'user': request.user}, instance=card)
        return render(request, 'frontend/card-create-form.html', {'form': form})


def tag_card_form(request, pk):
    card = Card.objects.get(pk=pk)

    if request.method == "POST":
        form = TagCheckboxForm(request.POST, context={'user': request.user}, instance=card)
        if form.is_valid():
            form.save()
            return HttpResponse("")
        else: 
            return render(request, 'frontend/partials/tag-card-form.html', {'form': form})
    else: 
        form = TagCheckboxForm(context={'user': request.user}, instance=card)
        return render(request, 'frontend/partials/tag-card-form.html', {'form': form})
    

#identical to tag_card_form but with different form. If i were a better coder I would make a common class or something (but honestly what's the point)
#I mean django already has the classes but ill be damned if I know how to use them.
def deck_card_form(request, pk):
    card = Card.objects.get(pk=pk)

    if request.method == "POST":
        form = DeckSelectForm(request.POST, context={'user': request.user}, instance=card)
        if form.is_valid():
            form.save()
            return HttpResponse("")
        else: 
            return render(request, 'frontend/partials/deck-card-form.html', {'form': form})
    
    else:
        form = DeckSelectForm(context={'user': request.user}, instance=card)
        return render(request, 'frontend/partials/deck-card-form.html', {'form': form})


def delete_card(request, pk):
    if request.method == "DELETE":
        Card.objects.get(pk=pk).delete()

        return HttpResponse("")
    

def delete_cards(request):
    if request.method == "POST":

        card_ids_str = request.POST.getlist('card_id')
        card_ids = [int(id) for id in card_ids_str]
        Card.objects.filter(pk__in=card_ids).delete()

        card_list = get_filtered_and_sorted_user_cards(request, True)

        return render(request, 'frontend/partials/cards.html', {'card_list': card_list})
    