from django import forms
from .models import Rout, Difficulty


class FilterForm(forms.Form):
    availible_choices = [i[0] for i in Rout.objects.values_list('difficulty').distinct()]
    choices = list()
    for choice in Difficulty.objects.values_list('id', 'name'):
        if choice[0] in availible_choices:
            choices.append(choice)

    min_distance = forms.IntegerField(initial=0)
    max_distance = forms.IntegerField(initial=1000)
    difficulty = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple())

