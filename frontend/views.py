
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django_htmx.http import HttpResponseClientRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timezone

from .models import *
from .forms import *
from .util import *

#TO NOT DO (because I have no time)
#complete success and error banners
#Double check all the form validation and stuff
#Make the Tag Filter look nicer (i tried...)
#Add Permissions to the models
#Anonymous Sign In
#The Play Mode
#Card Preview while making a card
#Text resizing for Cards depending on length of text
#optimise sql queries
#a search bar for cards

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
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

@login_required
def card_list_view(request):

    if request.htmx:
        template_name = 'frontend/partials/cards-and-tags.html'

    else:
        template_name = 'frontend/list.html'

    card_list = get_filtered_and_sorted_user_cards(request.GET, request.user)
    context = {'card_list': card_list}

    deck_id = int(request.GET.get('deck', 0))
    if deck_id != 0:
        context['deck'] = Deck.objects.get(pk=deck_id)

    tag_list = request.GET.getlist('filter')
    tag_list = Tag.objects.filter(pk__in=list(map(int, tag_list)))
    context['tag_list'] = tag_list
    context['form'] = TagSelectForm(context={'user': request.user})

    return render(request, template_name, context)

@login_required
def deck_list_view(request):

    if request.htmx:
        template_name = 'frontend/partials/decks.html'

    else:
        template_name = 'frontend/list.html'

    deck_list = get_sorted_user_decks(request.GET, request.user)

    return render(request, template_name, {'deck_list': deck_list})

@login_required
def deck_detail_view(request, pk):

    if request.htmx:
        return card_list_view(request)

    deck = Deck.objects.get(pk=pk)
    if deck.user != request.user:
        #add some error screen
        pass

    template_name = 'frontend/deck-detail.html'
    return render(request, template_name, {
        'deck': deck,
        'card_list': deck.cards.all()
    })


@login_required
def tag_select_list(request):

    form = TagSelectForm(context={'user': request.user})

    return render(request, 'frontend/partials/tag-select-list.html', {
        'form': form,
    })

@login_required
def add_tag(request):

    return render(request, 'frontend/partials/tag.html', {
        'tag': Tag.objects.get(pk=int(request.GET.get('tag')))
    })
    

def order_select_list(request):

    initial = request.GET.get('order_by', 'date_created')
    form = OrderSelectForm(initial={'order_by': initial})

    return render(request, 'frontend/partials/order-select-list.html', {
        'form': form,
    })


@login_required
def card_create_form(request):

    if request.method == "POST":
        form = CardForm(request.POST, context={'user': request.user})
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            next = request.POST.get('next', reverse("create_card"))
            if next == "":
                next = reverse("create_card")

            messages.success(request, 'Created!')
            return HttpResponseRedirect(next)
        else: 
            return render(request, 'frontend/card-create-form.html', {
                'form': form,
                'url': reverse_lazy('create_card'),
            })
    else: 

        if request.GET.get('deck', False):
            print('hi')
            initial_deck = Deck.objects.get(pk=request.GET.get('deck'))
        else:
            initial_deck=None
        
        form = CardForm(context={'user': request.user}, initial_deck=initial_deck)
        return render(request, 'frontend/card-create-form.html', {
            'form': form,
            'url': reverse_lazy('create_card'),
        })
    
@login_required
def card_update_form(request, pk):

    card = Card.objects.get(pk=pk)

    if request.method == "POST":
        form = CardForm(request.POST, context={'user': request.user}, instance=card)
        if form.is_valid():
            form.save()
            next = request.POST.get('next', reverse("card_list"))
            if next == "":
                next = reverse("card_list")

            messages.success(request, 'Updated!')
            return HttpResponseRedirect(next)
        else: 
            return render(request, 'frontend/card-create-form.html', {
                'form': form,
                'url': reverse_lazy('update_card', args=[pk]),
            })
    
    else:
        form = CardForm(context={'user': request.user}, instance=card)
        return render(request, 'frontend/card-create-form.html', {
            'form': form,
            'url': reverse_lazy('update_card', args=[pk]),
        })

@login_required
def deck_create_form(request):

    if request.method == "POST":
        form = DeckForm(request.POST, context={'user': request.user})
        if form.is_valid():
            form.instance.user = request.user
            form.save()

            messages.success(request, 'Created!')
            return HttpResponseRedirect(reverse('deck_list'))
        else: 
            return render(request, 'frontend/deck-create-form.html', {
                'form': form,
                'url': reverse_lazy('create_deck'),
            })
    else: 
        form = DeckForm(context={'user': request.user})
        return render(request, 'frontend/deck-create-form.html', {
            'form': form,
            'url': reverse_lazy('create_deck'),
        })


def deck_update_form(request, pk):

    deck = Deck.objects.get(pk=pk)

    if request.method == "POST":
        form = DeckForm(request.POST, context={'user': request.user}, instance=deck)
        if form.is_valid():
            form.save()
            next = request.POST.get('next', reverse("deck_list"))

            messages.success(request, 'Updated!')
            return HttpResponseRedirect(next)
        else: 
            return render(request, 'frontend/deck-create-form.html', {
                'form': form,
                'url': reverse_lazy('update_deck', args=[pk]),
            })
    
    else:
        form = DeckForm(context={'user': request.user}, instance=deck)
        return render(request, 'frontend/deck-create-form.html', {
            'form': form,
            'url': reverse_lazy('update_deck', args=[pk]),
        })


@login_required
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

@login_required
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
    
@login_required 
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
                'submit_url': reverse_lazy('deck_card_form', args=[pk]),
            })
    
    else:
        form = DeckSelectModelForm(context={'user': request.user}, instance=card)
        return render(request, 'frontend/modal-forms/deck-card-form.html', {
            'form': form,
            'submit_url': reverse_lazy('deck_card_form', args=[pk]),
        })
    
@login_required
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

@login_required
def remove_card(request, deck_pk, card_pk):

    deck = Deck.objects.get(pk=deck_pk)
    deck.cards.remove(card_pk)

    return HttpResponse("")

@login_required
def remove_card_multiple(request, pk):

    deck = Deck.objects.get(pk=pk)
    card_ids = request.POST.getlist('card_id')
    for id in card_ids:
        deck.cards.remove(id)

    return HttpResponseRedirect(reverse('card_list') + encode_params(request.POST))

@login_required
def tag_create_form(request):
    if request.method == "POST":

        form = TagForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            tag = form.save()

            form = TagSelectForm(context={'user': request.user})
            
            return render(request, 'frontend/partials/new-tag-option.html', {
                'tag': tag,
                'form': form,
            })

        else:
            return render(request, 'frontend/modal-forms/tag-create-form.html', {'form': form})


@login_required
def delete_tag(request, pk):
    Tag.objects.get(pk=pk).delete()

    form = TagSelectForm(context={'user': request.user})
            
    return render(request, 'frontend/partials/update-tags.html', {
        'form': form,
    })

@login_required
def delete_card(request, pk):
    if request.method == "DELETE":
        Card.objects.get(pk=pk).delete()

        return HttpResponse("")
    
@login_required
def delete_card_multiple(request):
    if request.method == "POST":

        card_ids = request.POST.getlist('card_id')
        card_ids = [int(id) for id in card_ids]
        Card.objects.filter(pk__in=card_ids).delete()

        return HttpResponseRedirect(reverse('card_list') + encode_params(request.POST))

@login_required
def delete_deck(request, pk):
    Deck.objects.get(pk=pk).delete()

    messages.success(request, 'Deleted Deck!')
    return HttpResponseRedirect(reverse('deck_list'))


@login_required
def deck_review(request, pk):
    deck = Deck.objects.get(pk=pk)
    page_num = request.GET.get("page", 1)

    if request.GET.get('new', False):
        cards = get_deck_review_cards(pk)
        request.session['deck_review_session'] = {
            'card_ids': [card.id for card in cards],
        }

        deck.date_last_reviewed = datetime.now()
        deck.save()
    
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

@login_required
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

@login_required
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

                cards_to_review = Card.objects.filter(pk__in=incorrect)
                return render(request, 'frontend/partials/learn-checkpoint.html', {
                    'deck': deck,
                    'cards': cards_to_review,
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


def update_messages(request):
    return render(request, 'frontend/partials/messages.html')