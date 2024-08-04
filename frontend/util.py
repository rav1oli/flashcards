from .models import *
from datetime import date

#CONFIDENCE_MATRIX[box][confidence (0 is confident, 4 is dont_know)] will give you the new box.
CONFIDENCE_MATRIX = [
    [2, 1, 0, 0],
    [3, 2, 0, 0],
    [4, 3, 1, 0],
    [4, 4, 2, 0],
    [5, 4, 2, 0],
    [6, 4, 2, 0],
    [6, 4, 2, 0],
]


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
    deck_id = int(request_data.get('deck', 0))
    
    card_list = get_user_cards(user)

    if deck_id != 0:
        card_list = card_list.filter(decks__id=deck_id)

    if tag_id == 0:
        return card_list.order_by(order_by)
    else:
        return card_list.filter(tags__id=tag_id).order_by(order_by)
    

def get_sorted_user_decks(request_data, user):
    
    order_by = request_data.get('order_by', 'date_created')

    deck_list = get_user_decks(user)

    return deck_list.order_by(order_by)


def calculate_result_times(card):
    
    boxes = ["Again", "Tomorrow", "2 days", "4 days", "1 week", "2 weeks", "1 month"]
    
    box = card.review_interval_box

    return [boxes[idx] for idx in CONFIDENCE_MATRIX[box]]


def update_card_review_time(card, confidence):
    box = card.review_interval_box

    if confidence == "confident":
        new_box = CONFIDENCE_MATRIX[box][0]

    elif confidence == "good":
        new_box = CONFIDENCE_MATRIX[box][1]

    elif confidence == "unsure":
        new_box = CONFIDENCE_MATRIX[box][2]
    
    else:
        new_box = CONFIDENCE_MATRIX[box][3]

    card.review_interval_box = new_box
    card.save()
    return


def encode_params(data):
    return f"?filter={data.get('filter', '0')}&order_by={data.get('order_by', 'date_created')}&deck={data.get('deck', '0')}"


def get_deck_review_cards(pk):
    return [card for card in Card.objects.filter(decks__id=pk) if date.today() >= card.get_review_date()]