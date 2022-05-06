from django import forms

class FilterForm(forms.Form):
    choices = [
        ('a', 'легкая'),
        ('b', 'средняя'),
        ('c', 'сложная'),
    ]
    min_distance = forms.IntegerField(initial=0)
    max_distance = forms.IntegerField(initial=1000)
    difficulty = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple())

