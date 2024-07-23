from .models import *
from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['title', 'description', 'cards']


class TagSelectForm(DynamicFormMixin, forms.Form):
    tags = DynamicField(
        forms.ModelChoiceField,
        queryset=lambda form: Tag.objects.filter(user=form.context['user']),
    )


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


class DeckSelectForm(DynamicFormMixin, form.ModelForm):
    decks = DynamicField()