
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import inlineformset_factory
from django_htmx.http import HttpResponseClientRedirect

from .models import *
from .forms import *
from .util import *

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


def deck_list_view(request):

    if request.htmx:
        template_name = 'frontend/partials/decks.html'

        order = request.GET.get('order_by', "date_created")
        request.session['preselected_order'] = order

    else:
        template_name = 'frontend/deck-list.html'

    deck_list = get_filtered_and_sorted_user_decks(request)

    return render(request, template_name, {'deck_list': deck_list})



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



def card_create_form(request):

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
    

def card_update_form(request, pk):

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


def deck_create_form(request):

    if request.method == "POST":
        form = DeckForm(request.POST, context={'user': request.user})
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('create_deck'))
        else: 
            return render(request, 'frontend/deck-create-form.html', {'form': form})
    else: 
        form = DeckForm(context={'user': request.user})
        return render(request, 'frontend/deck-create-form.html', {'form': form})


def tag_card_form(request, pk):

    card = Card.objects.get(pk=pk)

    if request.method == "POST":
        form = TagCheckboxModelForm(request.POST, context={'user': request.user}, instance=card)
        if form.is_valid():
            form.save()
            return HttpResponse("")
        else: 
            return render(request, 'frontend/modal-forms/tag-card-form.html', {
                'form': form,
                'submit_url': reverse_lazy('tag_card_form', args=[form.instance.pk]),
            })
    else: 
        form = TagCheckboxModelForm(context={'user': request.user}, instance=card)
        return render(request, 'frontend/modal-forms/tag-card-form.html', {
            'form': form,
            'submit_url': reverse_lazy('tag_card_form', args=[form.instance.pk]),
        })


def tag_card_multiple_form(request):

    if request.method == "POST":
        form = TagCheckboxForm(request.POST, context={'user': request.user})
        card_ids = request.POST.getlist('card_id')
        card_ids = [int(id) for id in card_ids]
        cards = Card.objects.filter(pk__in=card_ids)

        if form.is_valid():
            tags = form.cleaned_data.get('tags', [])
            for card in cards:
                for tag in tags:
                    card.tags.add(tag)

            return HttpResponse("")
        else: 
            return render(request, 'frontend/modal-forms/tag-card-form.html', {
                'form': form,
                'submit_url': reverse_lazy('tag_card_multiple_form')
            })
    
    else:
        form = TagCheckboxForm(context={'user': request.user})
        return render(request, 'frontend/modal-forms/tag-card-form.html', {
            'form': form,
            'submit_url': reverse_lazy('tag_card_multiple_form')
        })
    
    
def deck_card_form(request, pk):
    card = Card.objects.get(pk=pk)

    if request.method == "POST":
        form = DeckSelectModelForm(request.POST, context={'user': request.user}, instance=card)
        if form.is_valid():
            form.save()
            return HttpResponse("")
        else: 
            return render(request, 'frontend/modal-forms/deck-card-form.html', {
                'form': form,
                'submit_url': reverse_lazy('deck_card_form', args=[form.instance.pk])
            })
    
    else:
        form = DeckSelectModelForm(context={'user': request.user}, instance=card)
        return render(request, 'frontend/modal-forms/deck-card-form.html', {
            'form': form,
            'submit_url': reverse_lazy('deck_card_form', args=[form.instance.pk])
        })
    

def deck_card_multiple_form(request):

    if request.method == "POST":
        form = DeckSelectForm(request.POST, context={'user': request.user})
        card_ids = request.POST.getlist('card_id')
        card_ids = [int(id) for id in card_ids]
        cards = Card.objects.filter(pk__in=card_ids)

        if form.is_valid():
            decks = form.cleaned_data.get('decks', [])
            for card in cards:
                for deck in decks:
                    card.decks.add(deck)

            return HttpResponse("")
        else: 
            return render(request, 'frontend/modal-forms/deck-card-form.html', {
                'form': form,
                'submit_url': reverse_lazy('deck_card_multiple_form')
            })
    
    else:
        form = DeckSelectForm(context={'user': request.user})
        return render(request, 'frontend/modal-forms/deck-card-form.html', {
                'form': form,
                'submit_url': reverse_lazy('deck_card_multiple_form')
            })


def new_tag_form(request):
    if request.method == "POST":

        form = NewTagForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            tag = form.save()
            
            return render(request, 'frontend/partials/new-tag-checkbox-option.html', {'tag': tag})

        else:
            return render(request, 'frontend/modal-forms/new-tag-form.html', {'form': form})



def delete_card(request, pk):
    if request.method == "DELETE":
        Card.objects.get(pk=pk).delete()

        return HttpResponse("")
    

def delete_cards(request):
    if request.method == "POST":

        card_ids = request.POST.getlist('card_id')
        card_ids = [int(id) for id in card_ids]
        Card.objects.filter(pk__in=card_ids).delete()

        card_list = get_filtered_and_sorted_user_cards(request, True)

        return render(request, 'frontend/partials/cards.html', {'card_list': card_list})
    