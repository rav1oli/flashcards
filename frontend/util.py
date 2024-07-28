from .models import *


def get_user_cards(user):
    if user.is_authenticated:
        return Card.objects.filter(user=user)
    else:
        return Card.objects.none

    
def get_user_decks(user):
    if user.is_authenticated:
        return Deck.objects.filter(user=user)
    else:
        return Deck.objects.none


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
    

def get_filtered_and_sorted_user_decks(request, post=False):
    if post:
        order_by = request.POST.get('order_by', 'date_created')
    else:
        order_by = request.GET.get('order_by', 'date_created')

    deck_list = get_user_decks(request.user)

    return deck_list.order_by(order_by)


