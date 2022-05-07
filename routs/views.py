from django.views import generic
from django import forms
from django.shortcuts import render
from .forms import FilterForm
from .models import Rout, Difficulty
from django import forms
from django.db.models import Count


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    return render(request, 'index.html')


# class FilterForm(forms.Form):
#     availible_choices = [i[0] for i in Rout.objects.values_list('difficulty').distinct()]
#     choices = list()
#     for choice in Difficulty.objects.values_list('id', 'name'):
#         if choice[0] in availible_choices:
#             choices.append(choice)
#     print(choices)

#     min_distance = forms.IntegerField(initial=0)
#     max_distance = forms.IntegerField(initial=1000)
#     difficulty = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple())


class RoutListView(generic.ListView):
    # print(Rout.objects.values('difficulty').distinct().get())
    model = Rout

    def get(self, request):
        form = FilterForm()
        rout_list = Rout.objects.all()
        return render(request, 'routs/rout_list.html', {'form': form, 'rout_list': rout_list})


class UpdateRoutListView(generic.ListView):
    model = Rout

    def get(self, request):
        min_distance = request.GET.get('min_distance', 0)
        max_distance = request.GET.get('max_distance', 1000)
        difficulties = [int(i) for i in request.GET.get('difficulty')]

        rout_list = Rout.objects\
            .filter(distance__gte=min_distance)\
            .filter(distance__lte=max_distance)\
            .filter(difficulty__in=difficulties)

        return render(request, 'routs/update_rout_list.html', {'rout_list': rout_list})


class RoutDetailView(generic.DetailView):
    model = Rout