from django.urls import path
from .views import *

urlpatterns = [
    path("cards", CardList.as_view(), name="card_list"),
]

""" 
    path("", index, name="index"),
    path("deck/<int:deck_id>", deck_detail, name="deck_detail"),
    path("create_card", create_card, name="create_card"),
    path("edit_card/<int:card_id>", edit_card, name="edit_card"),
    path("create_deck", CreateDeckView.as_view(), name="create_deck"), 
"""