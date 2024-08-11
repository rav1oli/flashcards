
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django_htmx.http import HttpResponseClientRedirect
from django.core.paginator import Paginator

from .models import *
from .forms import *
from .util import *

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def index_view(request):
    decks = Deck.objects.all()
    deck_list = []
    for deck in decks:
        cards = get_deck_review_cards(deck.pk)
        deck_obj = {'deck': deck, 'cards': len(cards)}
        deck_list.append(deck_obj)

    return render(request, 'frontend/index.html', {
        'deck_list': deck_list
    })


def card_list_view(request):

    if request.htmx:
        template_name = 'frontend/partials/cards.html'

    else:
        template_name = 'frontend/list.html'

    card_list = get_filtered_and_sorted_user_cards(request.GET, request.user)
    context = {'card_list': card_list}

    deck_id = int(request.GET.get('deck', 0))
    if deck_id != 0:
        context['deck'] = Deck.objects.get(pk=deck_id)

    return render(request, template_name, context)


def deck_list_view(request):

    if request.htmx:
        template_name = 'frontend/partials/decks.html'

    else:
        template_name = 'frontend/list.html'

    deck_list = get_sorted_user_decks(request.GET, request.user)

    return render(request, template_name, {'deck_list': deck_list})


def deck_detail_view(request, pk):

    deck = Deck.objects.get(pk=pk)
    if deck.user != request.user:
        #add some error screen
        pass

    template_name = 'frontend/deck-detail.html'
    return render(request, template_name, {
        'deck': deck,
        'card_list': deck.cards.all()
    })



def tag_select_list(request):

    form = TagSelectForm(context={'user': request.user})

    return render(request, 'frontend/partials/tag-select-list.html', {
        'form': form,
    })
    

def order_select_list(request):

    initial = request.GET.get('order_by', 'date_created')
    form = OrderSelectForm(initial={'order_by': initial})

    return render(request, 'frontend/partials/order-select-list.html', {
        'form': form,
    })



def card_create_form(request):

    if request.method == "POST":
        form = CardForm(request.POST, context={'user': request.user})
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            next = request.POST.get('next', reverse("create_card"))
            if next == "":
                next = reverse("create_card")
            return HttpResponseRedirect(next)
        else: 
            return render(request, 'frontend/card-create-form.html', {'form': form})
    else: 

        if request.GET.get('deck'):
            initial_deck = Deck.objects.get(pk=request.GET.get('deck'))
        else:
            initial_deck=None
        
        form = CardForm(context={'user': request.user}, initial_deck=initial_deck)
        return render(request, 'frontend/card-create-form.html', {'form': form})
    

def card_update_form(request, pk):

    card = Card.objects.get(pk=pk)

    if request.method == "POST":
        form = CardForm(request.POST, context={'user': request.user}, instance=card)
        if form.is_valid():
            form.save()
            next = request.POST.get('next', reverse("card_list"))
            if next == "":
                next = reverse("card_list")
            return HttpResponseRedirect(next)
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
            return HttpResponseRedirect(reverse('deck_list'))
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


def remove_card(request, deck_pk, card_pk):

    deck = Deck.objects.get(pk=deck_pk)
    deck.cards.remove(card_pk)

    return HttpResponse("")


def remove_card_multiple(request, pk):

    deck = Deck.objects.get(pk=pk)
    card_ids = request.POST.getlist('card_id')
    for id in card_ids:
        deck.cards.remove(id)

    return HttpResponseRedirect(reverse('card_list') + encode_params(request.POST))


def tag_create_form(request):
    if request.method == "POST":

        form = TagForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            tag = form.save()
            
            return render(request, 'frontend/partials/new-tag-option.html', {'tag': tag})

        else:
            return render(request, 'frontend/modal-forms/tag-create-form.html', {'form': form})



def delete_tag(request, pk):
    Tag.objects.get(pk=pk).delete()

    return HttpResponse("")


def delete_card(request, pk):
    if request.method == "DELETE":
        Card.objects.get(pk=pk).delete()

        return HttpResponse("")
    

def delete_card_multiple(request):
    if request.method == "POST":

        card_ids = request.POST.getlist('card_id')
        card_ids = [int(id) for id in card_ids]
        Card.objects.filter(pk__in=card_ids).delete()

        return HttpResponseRedirect(reverse('card_list') + encode_params(request.POST))



def deck_studyaksjdaksjdbas(request, pk):
    cards = Card.objects.filter(decks__id=pk).order_by('date_created')
    p = Paginator(cards, 1)

    if request.htmx:
        template_name = 'frontend/partials/card-container.html' 
    else:
        template_name = 'frontend/deck-study.html'

    blank_history = {'results': {}, 'furthest': 1, 'current': 1}

    if request.method == "POST":
        
        history = request.session['deck_study_session']
        #save results
        for page_num, confidence in history['results'].items():
            update_card_review_time(cards[int(page_num) - 1], confidence)

        return HttpResponseClientRedirect(reverse('deck_detail', args=[pk]))
    
    else:
        

        #if navigated to via study button:
        if request.GET.get('new', False):
            history = blank_history
            request.session['deck_study_session'] = history #initialise deck_study_session obj
            page_num = 1
            page_obj = p.page(page_num)

        #if form changes, update history
        elif request.GET.get("change"):
            history = request.session.get('deck_study_session', blank_history)
            page_num = int(history['current'])

            history['results'][page_num] = request.GET.get('confidence', "dont_know")
            request.session['deck_study_session'] = history

        #navigated via arrows
        else:  
            page_num = int(request.GET.get('page', 1))
            history = request.session.get('deck_study_session', blank_history)
            history['current'] = page_num
            if page_num > history['furthest']:
                history['furthest'] = page_num

            request.session['deck_study_session'] = history

        page_obj = p.page(page_num)
        card = page_obj[0]
        result = history['results'].get(str(page_num), None)
        if result:
            form = ConfidenceForm(initial={'confidence': result})
            has_results = True
        else:
            form = ConfidenceForm()
            has_results = False

        has_next = "True" if history['furthest'] > page_num else "False"

        return render(request, template_name, {
            'deck': Deck.objects.get(pk=pk),
            'page_obj': page_obj,
            'card': card,
            'result_times': calculate_result_times(card),
            'form': form,
            'has_results': has_results,
            'has_next': has_next,
        })


def deck_review(request, pk):
    deck = Deck.objects.get(pk=pk)
    page_num = request.GET.get("page", 1)

    if request.GET.get('new', False):
        cards = get_deck_review_cards(pk)
        request.session['deck_review_session'] = {
            'card_ids': [card.id for card in cards],
        }
    
    else:
        session = request.session.get('deck_review_session', {})
        cards = Card.objects.filter(pk__in=session.get('card_ids', [])).order_by('date_created')
        
    p = Paginator(cards, 1)
        
    page_obj = p.get_page(page_num)

    if request.method == "POST":
        card = Card.objects.get(pk=request.POST.get('card_id'))
        confidence = request.POST.get('confidence', 'dont_know')
        
        update_card_review_time(card, confidence)

        page_num = int(request.POST.get('page_num', 1))
        if page_num < p.count:
            return HttpResponseRedirect(reverse('deck_review', args=[deck.id]) + '?page=' + str(page_num + 1))
        else:
            return HttpResponseClientRedirect(reverse('index'))

    if request.htmx:
        template_name = 'frontend/partials/review-card-container.html' 
    else:
        template_name = 'frontend/deck-review.html'

    return render(request, template_name, {
        'deck': Deck.objects.get(pk=pk),
        'page_obj': page_obj,
        'card': page_obj[0],
        'result_times': calculate_result_times(page_obj[0]),
        'form': ConfidenceForm(),
    })


def deck_study(request, pk):
    cards = Card.objects.filter(decks__id=pk).order_by('date_created')
    p = Paginator(cards, 1)

    if request.htmx:
        template_name = 'frontend/partials/study-card-container.html' 
    else:
        template_name = 'frontend/deck-study.html'

    page_number = request.GET.get("page", 1)
    page_obj = p.get_page(page_number)

    return render(request, template_name, {
        'deck': Deck.objects.get(pk=pk),
        'page_obj': page_obj,
        'card': page_obj[0],
    })


def deck_learn(request, pk):
    deck = Deck.objects.get(pk=pk)
    page_num = request.GET.get("page", 1)

    if request.GET.get('new', False):
        incorrect = [] # list of card_ids they got wrong
        cards = deck.cards.all().order_by('date_created')
        request.session['deck_learn_session'] = {
            'incorrect': incorrect,
            'cards': [card.id for card in cards],
        }   

    else:
        session = request.session.get('deck_learn_session', {})
        incorrect = session.get('incorrect', [])
        cards = Card.objects.filter(id__in=request.session['deck_learn_session']['cards']).order_by('date_created')
        
    p = Paginator(cards, 1)
        
    page_obj = p.get_page(page_num)

    if request.method == "POST":
        card_id = request.POST.get('card_id')
        response = request.POST.get('response', 'incorrect') # response is 'correct' or 'incorrect'

        if response == 'incorrect':
            incorrect.append(card_id)
            session = request.session['deck_learn_session']
            session['incorrect'] = incorrect
            request.session['deck_learn_session'] = session

        page_num = int(request.POST.get('page_num', 1))

        if page_num < p.count:
            return HttpResponseRedirect(reverse('deck_learn', args=[deck.id]) + '?page=' + str(page_num + 1))
        else:
            if len(incorrect) > 0:
                request.session['deck_learn_session'] = {
                    'incorrect': [],
                    'cards': incorrect,
                }
                return render(request, 'frontend/partials/learn-checkpoint.html', {
                    'deck': deck,
                })
            else:
                return HttpResponseClientRedirect(reverse('deck_detail', args=[deck.id]))

    if request.htmx:
        template_name = 'frontend/partials/learn-card-container.html' 
    else:
        template_name = 'frontend/deck-learn.html' # same template as review (for now)

    return render(request, template_name, {
        'deck': Deck.objects.get(pk=pk),
        'page_obj': page_obj,
        'card': page_obj[0],
        'incorrect_num': len(incorrect),
    })


def delete(request):
    return HttpResponse(status=201)