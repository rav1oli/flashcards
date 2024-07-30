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


def get_filtered_and_sorted_user_cards(request_data, user):

    order_by = request_data.get('order_by', 'date_created')
    tag_id = int(request_data.get('filter', 0))
    deck = request_data.get('deck_id', 0)
    
    card_list = get_user_cards(user)

    if deck != 0:
        card_list = card_list.filter(decks=deck)

    if tag_id == 0:
        return card_list.order_by(order_by)
    else:
        return card_list.filter(tags__id=tag_id).order_by(order_by)
    

def get_sorted_user_decks(request_data, user):
    
    order_by = request_data.get('order_by', 'date_created')

    deck_list = get_user_decks(user)

    return deck_list.order_by(order_by)
