from django import forms
from django.views import generic
from django.shortcuts import render
from django.db.models import Min, Max
from django.core.paginator import Paginator
from .forms import FilterForm
from .models import Rout, Difficulty, Surface, Direction, Tag, RouteCollections


def index(request):
    """
    Home page rendering
    """
    route_collections = RouteCollections.objects.all()

    return render(request, 'index.html', {'route_collections': route_collections})


class RoutListView(generic.ListView):
    model = Rout

    def get(self, request):
        """
        Render page of routes searching.
        Firstly parse params for filter from request,
        if param was not given - return all available values in data base.
        Then render page with request parameters.
        """
        
        distance_range = Rout.objects.aggregate(Min('distance'), Max('distance'), Max('distance_max'))
        _min1 = distance_range['distance__min'] or 0
        _max1 = distance_range['distance__max'] or 0
        _max2 = distance_range['distance_max__max'] or 0

        _min_distance = request.GET.get('min_distance')
        if _min_distance == None:
            _min_distance = _min1

        _max_distance = request.GET.get('max_distance')
        if _max_distance == None:
            _max_distance = max(_max1, _max2)

        choice_params = dict()
        params = ['difficulty', 'surface', 'direction', 'tags']
        models = [Difficulty, Surface, Direction, Tag]
        for param, model in zip(params, models):
            _param = request.GET.get(param)
            if _param == None:
                _param = 'all'
            choice_params.update(dict({param: _param}))

        _is_transport_availability = request.GET.get('is_transport_availability')
        if _is_transport_availability == None:
            _is_transport_availability = 'unknown'

        form = FilterForm()

        class FilterView():
            def __init__(self, field_id, title, form):
                self.field_id = field_id
                self.title = title
                self.form = form

        fields = dict(difficulty='Сложность', surface='Тип', direction='Направление', tags='Особенности')
        filter_views = list()
        for field_id in fields.keys():
            filter_views.append(FilterView(field_id, fields[field_id], form[field_id]))

        return render(request, 'routs/rout_list.html', {
            'form': form,
            'filter_views': filter_views,
            'min_distance': _min_distance,
            'max_distance': _max_distance,
            'difficulty': choice_params['difficulty'],
            'surface': choice_params['surface'],
            'direction': choice_params['direction'],
            'tags': choice_params['tags'],
            'is_transport_availability': _is_transport_availability
        })


class UpdateRoutListView(generic.ListView):
    def get_multiple_choice_search_param(self, request, param):
        search_param = request.GET.get(param)
        if search_param == None or search_param == 'all':
            return Rout.get_available_choices(param)
        else:
            return [int(i) for i in search_param.split('_')]

    def get(self, request):
        page = int(request.GET.get('page', 1))
        min_distance = int(request.GET.get('min_distance', 1))
        max_distance = int(request.GET.get('max_distance', 1000))
        difficulties = self.get_multiple_choice_search_param(request, 'difficulty')
        surfaces = self.get_multiple_choice_search_param(request, 'surface')
        directions = self.get_multiple_choice_search_param(request, 'direction')
        tags = self.get_multiple_choice_search_param(request, 'tags')
        is_transport_availability = request.GET.get('is_transport_availability')

        if is_transport_availability == 'true':
            transport_availabilities = [True]
        elif is_transport_availability == 'false':
            transport_availabilities = [False]
        else:
            transport_availabilities = [True, False]

        if min_distance == 0:
            min_distance = 1

        route_list = Rout.get_filtered_routes(min_distance, max_distance, difficulties, surfaces, directions, tags, transport_availabilities)
        page_obj = Paginator(route_list, 10).page(page)

        return render(request, 'routs/update_rout_list.html', dict(rout_list=route_list, page_obj=page_obj))


class RoutDetailView(generic.DetailView):
    model = Rout