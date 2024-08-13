from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/signup/', views.SignUpView.as_view(), name="signup"),

    path("", views.index_view, name="index"),
    #path("cards", views.CardListTemplateView.as_view(), name="cards"),
    path("create_card", views.card_create_form, name="create_card"),
    path("update_card/<pk>", views.card_update_form, name="update_card"),
    path("create_deck", views.deck_create_form, name="create_deck"),

    path("card_list", views.card_list_view, name="card_list"),
    path("deck_list", views.deck_list_view, name="deck_list"),
    path("deck/<int:pk>", views.deck_detail_view, name="deck_detail"),

    path("tag_select_list", views.tag_select_list, name="tag_select_list"),
    path("tag_select_form", views.tag_select_form, name="tag_select_form"),
    # path("add_tag", views.add_tag, name="add_tag"),
    path("order_select_list", views.order_select_list, name="order_select_list"),
    
    path("add_tags_to_card/<pk>", views.tag_card_form, name="tag_card_form"),
    path("add_tags_to_cards", views.tag_card_multiple_form, name="tag_card_multiple_form"),
    path("add_cards_to_deck/<pk>", views.deck_card_form, name="deck_card_form"),
    path("add_cards_to_decks", views.deck_card_multiple_form, name="deck_card_multiple_form"),
    path("remove_card_from_deck/<int:deck_pk>/<int:card_pk>", views.remove_card, name="remove_card"),
    path("remove_cards_from_decks/<int:pk>", views.remove_card_multiple, name="remove_card_multiple"),
    path("create_tag", views.tag_create_form, name="tag_create_form"),
    path("delete_tag/<pk>", views.delete_tag, name="delete_tag"),

    path("delete_card/<pk>", views.delete_card, name="delete_card"),
    path("delete_cards", views.delete_card_multiple, name="delete_card_multiple"),
    path("delete", views.delete, name="delete"),

    path("deck_study/<pk>", views.deck_study, name="deck_study"),
    path("deck_review/<pk>", views.deck_review, name="deck_review"),
    path("deck_learn/<pk>", views.deck_learn, name="deck_learn"),
]

""" 
    path("", index, name="index"),
    path("deck/<int:deck_id>", deck_detail, name="deck_detail"),
    path("create_card", create_card, name="create_card"),
    path("edit_card/<int:card_id>", edit_card, name="edit_card"),
    path("create_deck", CreateDeckView.as_view(), name="create_deck"), 
"""