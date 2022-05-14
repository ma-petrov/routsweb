from django.views import generic
from django import forms
from django.shortcuts import render
from .forms import FilterForm
from .models import Rout, Difficulty
from django import forms
from django.db.models import Count, Q


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
        return render(request, 'routs/rout_list.html', {
            'form': form,
            'rout_list': rout_list,
            'choice_form_fields': [
                ('difficulty', 'Сложность'),
                ('direction', 'Направление'),
                ('tag', 'Особенности')
            ]
        })


class UpdateRoutListView(generic.ListView):
    model = Rout

    def get(self, request):
        min_distance = int(request.GET.get('min_distance', 1))
        max_distance = int(request.GET.get('max_distance', 1000))
        difficulties = [int(i) for i in request.GET.get('difficulty')]
        surfaces = [int(i) for i in request.GET.get('surface')]
        directions = [int(i) for i in request.GET.get('direction')]
        tags = [int(i) for i in request.GET.get('tag')]
        is_transport_availability = request.GET.get('is_transport_availability')

        if is_transport_availability == 'true':
            is_transport_availabilities = [True]
        elif is_transport_availability == 'false':
            is_transport_availabilities = [False]
        else:
            is_transport_availabilities = [True, False]

        if min_distance == 0:
            min_distance = 1

        rout_list = Rout.objects.filter(
            (Q(distance__range=(min_distance, max_distance)) | Q(distance_max__range=(min_distance, max_distance))) &
            Q(difficulty__in=difficulties) &
            Q(surface__in=surfaces) &
            Q(direction__in=directions) &
            Q(tags__in=tags) &
            Q(is_transport_availability__in=is_transport_availabilities)
        ).distinct()

        return render(request, 'routs/update_rout_list.html', {'rout_list': rout_list})


class RoutDetailView(generic.DetailView):
    model = Rout