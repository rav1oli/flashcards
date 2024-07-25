from .models import *


def get_user_cards(user):
    if user.is_authenticated:
        return Card.objects.filter(user=user)
    else:
        return Card.objects.none


