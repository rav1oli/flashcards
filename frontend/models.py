
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    front = models.TextField()
    back = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_last_reviewed = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="cards")
    #add option for file upload later

    def __str__(self):
        return self.front

class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    cards = models.ManyToManyField(Card, blank=True, related_name="decks")
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now_add=True)
    date_last_reviewed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DeckForm(ModelForm):
    class Meta:
        model = Deck
        fields = ['title', 'description', 'cards']