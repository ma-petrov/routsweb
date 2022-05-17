from django import forms
from .models import Rout, Difficulty, Surface, Direction, Tag


class FilterForm(forms.Form):
    def __init__(self):
        super(FilterForm, self).__init__()

        min_distance = forms.IntegerField(initial=0)
        min_distance.widget.attrs.update({'class': 'input-number'})
        self.fields.update(dict(min_distance=min_distance))
        
        max_distance = forms.IntegerField(initial=1000)
        max_distance.widget.attrs.update({'class': 'input-number'})
        self.fields.update(dict(max_distance=max_distance))

        difficulty = self.create_choice_form('difficulty', Difficulty)
        self.fields.update(dict(difficulty=difficulty))

        surface = self.create_choice_form('surface', Surface)
        self.fields.update(dict(surface=surface))

        direction = self.create_choice_form('direction', Direction)
        self.fields.update(dict(direction=direction))

        tag = self.create_choice_form('tags', Tag)
        self.fields.update(dict(tag=tag))

        is_transport_availability = forms.BooleanField(required=False)
        is_transport_availability.widget = forms.NullBooleanSelect(attrs={'class': 'boolean-choice'})
        self.fields.update(dict(is_transport_availability=is_transport_availability))

    def get_choices(self, field, model):
        available_choices = [i[0] for i in Rout.objects.values_list(field).distinct()]
        choices = list()
        for choice in model.objects.values_list('id', 'name'):
            if choice[0] in available_choices:
                choices.append(choice)
        return choices

    def create_choice_form(self, field, model):
        return forms.MultipleChoiceField(choices=self.get_choices(field, model), widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'drop-down-multiple-choice-list-content'}
        ))