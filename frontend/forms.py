from .models import *
from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin

class DeckForm(forms.ModelForm):

    class Meta:
        model = Deck
        fields = ['title', 'description', 'cards']


class CardForm(DynamicFormMixin, forms.ModelForm):

    decks = DynamicField(
        forms.ModelMultipleChoiceField,
        queryset=lambda form: Deck.objects.filter(user=form.context['user']),
        widget=lambda _: forms.CheckboxSelectMultiple,
        required=False,
    )

    tags = DynamicField(
        forms.ModelMultipleChoiceField,
        queryset=lambda form: Tag.objects.filter(user=form.context['user']),
        widget=lambda _: forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Card
        fields = ['front', 'back', 'tags', 'decks']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            initial_decks = self.instance.decks.all()
            self.fields['decks'].initial = initial_decks


    def save(self, commit=True):
        # Retrieve the card instance being saved
        card_instance = super().save(commit=False)
        
        # If the instance is saved, update the many-to-many relationship
        if commit:
            card_instance.save()
        
        decks_selected = self.cleaned_data.get('decks', [])
        card_instance.decks.set(decks_selected)

        tags_selected = self.cleaned_data.get('tags', [])
        card_instance.tags.set(tags_selected)
        
        return card_instance
    

class TagSelectForm(DynamicFormMixin, forms.Form):
    tags = DynamicField(
        forms.ModelChoiceField,
        queryset=lambda form: Tag.objects.filter(user=form.context['user']),
        empty_label=None,
    )


class OrderSelectForm(forms.Form):
    ORDER_CHOICES = [
        ("date_created", "Oldest"),
        ("-date_created", "Newest"),
        ("date_edited", "Least Recently Edited"),
        ("-date_edited", "Most Recently Edited"),
        ("date_reviewed", "Least Recently Reviewed"),
        ("-date_reviewed", "Most Recently Reviewed"),
    ]

    order_by = forms.ChoiceField(choices=ORDER_CHOICES)


class TagCheckboxForm(DynamicFormMixin, forms.ModelForm):
    tags = DynamicField(
        forms.ModelMultipleChoiceField,
        queryset=lambda form: Tag.objects.filter(user=form.context['user']),
        widget=lambda _: forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Card
        fields = ['tags']


class DeckSelectForm(DynamicFormMixin, forms.ModelForm):

    class Meta:
        model = Card
        fields = ['decks']

    decks = DynamicField(
        forms.ModelMultipleChoiceField,
        queryset=lambda form: Deck.objects.filter(user=form.context['user']),
        widget=lambda _: forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            initial_decks = self.instance.decks.all()
            self.fields['decks'].initial = initial_decks


    def save(self, commit=True):
        # Retrieve the card instance being saved
        card_instance = super().save(commit=False)
        
        # If the instance is saved, update the many-to-many relationship
        if commit:
            card_instance.save()
        
        decks_selected = self.cleaned_data.get('decks', [])
        card_instance.decks.set(decks_selected)
        
        return card_instance



    

    