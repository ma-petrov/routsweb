from django import forms
from .models import Rout, Difficulty, Surface, Direction, Tag

class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, title):
        super(CustomCheckboxSelectMultiple, self).__init__()
        self.title = title

    def render(self, name=None, value=None, attrs=None, renderer=None):
        choice = '''
        <div class="drop-down-multiple-choice-content">
            <input type="checkbox" name="{name}" value="{value}" class="drop-down-multiple-choice-checkbox" id="id_{name}_{i}">
            <div class="drop-down-multiple-choice-label">
                <label for="id_{name}_{i}">{label}</label>
            </div>
        </div>
        '''

        widget = '''
        <div class="filter-container">
            <div class="filter-item-title">{title}</div>
            <div class="drop-down-multiple-choice-button-contaniner">
                <input type="button" class="drop-down-multiple-choice-button" id="drop-down-multiple-choice-button-{name}" value="Все">
            </div>
            <div class="drop-down-multiple-choice-list-container" id="drop-down-multiple-choice-list-container-{name}" style="display: none;">
                <div id="id_{name}">{content}</div>
            </div>
        </div>
        '''

        optgroups = [optgroup[1][0] for optgroup in self.get_context(name, value, attrs)["widget"]["optgroups"]]
        content = ''.join([choice.format(i=i, name=o['name'], value=o['value'], label=o['label']) for i, o in enumerate(optgroups)])
        return widget.format(title=self.title, name=name, content=content)

class FilterForm(forms.Form):
    def __init__(self):
        super(FilterForm, self).__init__()

        min_distance = forms.IntegerField(initial=0)
        min_distance.widget.attrs.update({'class': 'input-number'})
        self.fields.update(dict(min_distance=min_distance))
        
        max_distance = forms.IntegerField(initial=1000)
        max_distance.widget.attrs.update({'class': 'input-number'})
        self.fields.update(dict(max_distance=max_distance))

        self.fields.update(dict(difficulty=self.create_choice_form('difficulty', Difficulty, 'Сложность')))
        self.fields.update(dict(surface=self.create_choice_form('surface', Surface, 'Тип')))
        self.fields.update(dict(direction=self.create_choice_form('direction', Direction, 'Направление')))
        self.fields.update(dict(tags=self.create_choice_form('tags', Tag, 'Особенности')))

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

    def create_choice_form(self, field, model, title):
        return forms.MultipleChoiceField(choices=self.get_choices(field, model), widget=CustomCheckboxSelectMultiple(title))