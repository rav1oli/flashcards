# Flashcards

A flashcard website where users can create and manage flashcards and study and review decks of cards (similar to anki and quizlet)

## How To Run 

Use
```
python manage.py runserver
```

## Distinctiveness and Complexity

The project is clearly distinct from other projects in the course, not sharing much with the Mail API, Commerce site or Networking site.

It is also substantially more complex. The '/cards' view alone allows sorting and filtering the cards, as well as editing their tags and the decks they're contained in with modal forms in a SPA format. 

Other views include the deck list, creating cards with an interactive preview, creating decks, a deck detail view, and an index view where the user can see the decks due for review that day.

The project also includes a view for decks and 3 options to study them: 'Study', 'Learn', and 'Review': 
- Study just lets the user see flashcards one by one with a paginated list view
- Learn gets asks the user whether they got the card right or not, re-displaying the incorrect cards.
- Review uses a spaced repetition algorithm to display cards after different lengths of time depending on the confidence (same as anki)

The project is complete with 3 custom models (Tags, Cards, and Decks), custom styling and animations, an interactive UI with CSS and JavaScript, and a mobile responsive layout.

## Documentation

### Technology Choice

The project went through several iterations using different technologies:
- First I used React, but struggled to effectively use it with Django so abandonded it. 
- I then tried switched to plain Javascript with a simple REST API using Django Rest Framework but found it very difficult to maintain and build upon my code (and found myself writing far more of it than I felt I needed).
- Finally (after a holiday and wanting to restart) I rebuilt the site with HTMX, shifting most of the work to the backend. Since it works excellently with Django everything went smoothly from there.

For styling I opted for Tailwind after trying both plain CSS and Bootstrap. Bootstrap I found tedious to learn and too difficult to customize and I found writing CSS or Sass too slow (naming things is the most difficult part of programming afterall). Tailwind struck the right balance for me.

Other technologies I used were Django-Htmx, Django Widget Tweaks, Django Forms Dynamic, and still a lot of plain Javascript where it was easier than HTMX. (e.g for the interactive preview when creating a card in 'templates/frontend/create-card-form')

### Files

- views.py does most of the heavy lifting as it handles responses to HTMX requests by rendering various partial templates (in 'templates/frontend/partials').
- util.py contains some helper functions.
- forms.py contains all the forms, which required a lot of customisation to work with reverse many-to-many relationships.
- templatetags contains a few custom tags where I needed them.
- static contains the css and various icons used in the project.

This took me... far too long but I'm happy with the end result. There are a lot of things that I want to add or improve upon (a short list of which is commented in views.py) but it's time to take what I've learned and move on to another project. Thank you for reading.