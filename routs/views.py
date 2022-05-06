from django.views import generic
from django import forms
from django.shortcuts import render
from .models import Rout
from .forms import FilterForm
from django.db.models import Count


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    return render(request, 'index.html')


class RoutListView(generic.ListView):
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
        easy = request.GET.get('difficulty_a')
        medium = request.GET.get('difficulty_b')
        hard = request.GET.get('difficulty_c')

        difficulties = list()
        if easy == 'false' and medium == 'false' and hard == 'false':
            difficulties = [1, 2, 3]
        else:
            if easy == 'true': difficulties.append(1)
            if medium == 'true': difficulties.append(2)
            if hard == 'true': difficulties.append(3)

        # difficulties = ''
        # if easy == 'false' and medium == 'false' and hard == 'false':
        #     difficulties = ['легкая', 'средняя', 'сложная']
        # else:
        #     if easy == 'true': difficulties += 'легкая'
        #     if medium == 'true': difficulties += 'средняя'
        #     if hard == 'true': difficulties += 'сложная'

        print(Rout.objects.values('difficulty', entries=Count('title')))

        rout_list = Rout.objects\
            .filter(distance__gte=min_distance)\
            .filter(distance__lte=max_distance)\
            .filter(difficulty__in=difficulties)
            # .filter(distance__in=difficulties)
        return render(request, 'routs/update_rout_list.html', {'rout_list': rout_list})


class RoutDetailView(generic.DetailView):
    model = Rout