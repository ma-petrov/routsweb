from django import forms
from .models import Rout, Difficulty, Surface, Direction, Tag


class FilterForm(forms.Form):
    def create_choice_form(field, model):
        available_choices = [i[0] for i in Rout.objects.values_list(field).distinct()]
        choices = list()
        for choice in model.objects.values_list('id', 'name'):
            if choice[0] in available_choices:
                choices.append(choice)
        return forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'drop-down-multiple-choice-list-content'}
        ))

    min_distance = forms.IntegerField(initial=0)
    min_distance.widget.attrs.update({'class': 'input-number'})

    max_distance = forms.IntegerField(initial=1000)
    max_distance.widget.attrs.update({'class': 'input-number'})

    difficulty = create_choice_form('difficulty', Difficulty)

    surface = create_choice_form('surface', Surface)

    direction = create_choice_form('direction', Direction)

    tag = create_choice_form('tags', Tag)

    is_transport_availability = forms.BooleanField(required=False, widget=forms.NullBooleanSelect(
        attrs={'class': 'boolean-choice'}
    ))


