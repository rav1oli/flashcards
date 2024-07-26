from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/signup/', views.SignUpView.as_view(), name="signup"),

    path("", views.IndexView.as_view(), name="index"),
    #path("cards", views.CardListTemplateView.as_view(), name="cards"),
    path("create_card", views.create_card_form, name="create_card"),
    path("update_card/<pk>", views.update_card_form, name="update_card"),

    path("card_list", views.card_list_view, name="card_list"),
    path("tag_select_list", views.tag_select_list, name="tag_select_list"),
    path("order_select_list", views.order_select_list, name="order_select_list"),
    

    path("tag_card_form/<pk>", views.tag_card_form, name="tag_card_form"),
    path("deck_card_form/<pk>", views.deck_card_form, name="deck_card_form"),

    path("delete_card/<pk>", views.delete_card, name="delete_card"),
    path("delete_cards", views.delete_cards, name="delete_cards"),
]

""" 
    path("", index, name="index"),
    path("deck/<int:deck_id>", deck_detail, name="deck_detail"),
    path("create_card", create_card, name="create_card"),
    path("edit_card/<int:card_id>", edit_card, name="edit_card"),
    path("create_deck", CreateDeckView.as_view(), name="create_deck"), 
"""