from user_agents import parse
from django import forms
from django.views import generic
from django.shortcuts import render
from django.db.models import Min, Max
from django.core.paginator import Paginator
from .forms import FilterForm
from .models import Rout, Difficulty, Surface, Direction, Tag, RouteCollections
from .utils import Bunch


class SearchParam:
    """
    Abstract class for request params parsing, validation and redering.
    """

    def __init__(self, param):
        self.param = param

    def parse_search_param(self):
        raise Exception("Method parse_search_param is not implemented!")
    
    def get_clean_param(self, request):
        return Rout.get_valid_param_value(self.param, self.parse_search_param(request))


class NumericSearchParam(SearchParam):
    """
    Numeric search param validation and generation.
    """

    def parse_search_param(self, request):
        value = request.GET.get(self.param)
        if value != None:
            return int(value)
        else:
            return None


class ChoiceSearchParam(SearchParam):
    """
    Choice search param validation and generation.
    """

    def parse_search_param(self, request):
        value = request.GET.get(self.param)
        if value != None and value != 'all':
            return value.split('_')
        else:
            return None


class BooleanSearchParam(SearchParam):
    """
    Boolean search param validation and generation.
    """

    def parse_search_param(self, request):
        value = request.GET.get(self.param)
        if value in ['true', 'false']:
            return dict(true=[True], false=[False])[value]
        else:
            return [True, False]

class SearchParamListFacroty():

    SEARCH_PARAMS = Rout.FILTER_PARAMS

    @classmethod
    def create_param(cls, param):
        if param in Rout.NUMERIC_PARAMS:
            return NumericSearchParam(param)
        elif param in Rout.CHOICE_PARAMS:
            return ChoiceSearchParam(param)
        elif param in Rout.BOOLEAN_PARAMS:
            return BooleanSearchParam(param)
        else:
            raise(f"param is expected to be one of {cls.SEARCH_PARAMS}")


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

        collection = request.GET.get('collection', -1)
        if collection != -1:
            search_params = RouteCollections.objects.get(id=collection).get_params()
        else:
            search_params = r"{}"

        return render(request, 'routs/rout_list.html', dict(form=FilterForm(), search_params=search_params))


class UpdateRoutListView(generic.ListView):
    def get(self, request):
        # if parse(request.META['HTTP_USER_AGENT']).is_mobile:
        #     pagination_buttons = Bunch(dict(home="", prev="", next="", last=""))
        # else:
        #     pagination_buttons = Bunch(dict(home="В начало", prev="Назад", next="Вперёд", last="В конец"))

        page = int(request.GET.get('page', 1))

        params = dict()
        for param in SearchParamListFacroty.SEARCH_PARAMS:
            params.update({param: SearchParamListFacroty.create_param(param).get_clean_param(request)})

        route_list = Rout.get_filtered_routes(**params)
        page_obj = Paginator(route_list, 10).page(page)

        # context = dict(rout_list=route_list, page_obj=page_obj, pagination_buttons=pagination_buttons)
        # return render(request, 'routs/update_rout_list.html', context)
        return render(request, 'routs/update_rout_list.html', dict(rout_list=route_list, page_obj=page_obj))


class RoutDetailView(generic.DetailView):
    model = Rout