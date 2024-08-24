
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import timedelta

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

    #based on the tailwind classes, second parameter is the no. of characters for each break point.
    FONT_SIZE_CHOICES = [
        ("text-base", "216"),
        ("text-lg", "192"),
        ("text-xl", "128"),
        ("text-2xl", "0"),
    ]

    #time intervals corresponding with each box.
    TIME_INTERVALS = [timedelta(0), timedelta(days=1), timedelta(days=2), timedelta(days=4), timedelta(days=7), timedelta(days=14), timedelta(days=30)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    front = models.TextField(max_length=310)
    front_font_size = models.CharField(choices=FONT_SIZE_CHOICES, max_length=16, default="text-2xl")
    back = models.TextField(max_length=310)
    back_font_size = models.CharField(choices=FONT_SIZE_CHOICES, max_length=16, default="text-2xl")
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_last_reviewed = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="cards")
    review_interval_box = models.PositiveSmallIntegerField(choices=REVIEW_INTERVAL_CHOICES, default=0)

    def __str__(self):
        return self.front

    def get_review_date(self):
        return self.date_last_reviewed.date() + self.TIME_INTERVALS[self.review_interval_box]
        


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
    
    

