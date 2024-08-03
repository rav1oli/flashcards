
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django import forms

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Card(models.Model):
    '''
    First number is the box, 2nd number is the when next review should occur.
     - Confident increases box num by 2 up to box.
     - Good increases box num by 1 until 1 week.
     - Unsure decreases box num by 1, after 1 week decrease by 2.
     - Don't Know brings back to box 0.
    '''
    REVIEW_INTERVAL_CHOICES = [
        (0, "Again"),
        (1, "Tomorrow"),
        (2, "2 days"),
        (3, "4 days"),
        (4, "1 week"),
        (6, "2 weeks"),
        (7, "1 month"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    front = models.TextField()
    back = models.TextField()
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_last_reviewed = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="cards")
    review_interval_box = models.PositiveSmallIntegerField(choices=REVIEW_INTERVAL_CHOICES, default=0)

    def __str__(self):
        return self.front


class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()

    cards = models.ManyToManyField('Card', blank=True, related_name="decks")
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now_add=True)
    date_last_reviewed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    

