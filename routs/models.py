from json import dumps
from django.db import models
from django.urls import reverse
from django.db.models import Count, Q, Min, Max
from .utils import Bunch

class Availability(models.Model):
    """
    Model
    """
    name = models.CharField(max_length=7)

    def __str__(self):
        """
        String for representing the object.
        """
        return self.name


class Difficulty(models.Model):
    """
    Difficulty represents is rout easy, medium or hard
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the object.
        """
        return self.name


class Surface(models.Model):
    """
    Surface reporsents type of road
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the object.
        """
        return self.name


class Direction(models.Model):
    """
    Direction represents the location of the route relative to the city
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the object.
        """
        return self.name


class Tag(models.Model):
    """
    Tag represents characteristic of the rout
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the object.
        """
        return self.name


class Rout(models.Model):
    """
    Model representing a Rout.
    """

    title = models.CharField(max_length=200)
    distance = models.PositiveIntegerField(help_text="Enter distance in kilometers, or min distance if range")
    distance_max = models.PositiveIntegerField(null=True, help_text="If range - enter max distance, else - enter 0")
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)
    surface = models.ForeignKey(Surface, on_delete=models.SET_NULL, null=True)
    direction = models.ManyToManyField(Direction)
    is_transport_availability = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, help_text="Select characteristics")
    description = models.CharField(max_length=1000)
    goggle_map_link = models.CharField(max_length=200)
    google_map_foreign_link = models.CharField(max_length=200)
    kommot_map_link = models.CharField(max_length=200)
    bike_map_link = models.CharField(max_length=200)
    kml_file_link = models.CharField(max_length=200)
    wallpaper_image = models.ImageField(upload_to='uploads/', null=True)

    NUMERIC_PARAMS = ['min_distance', 'max_distance']
    CHOICE_PARAMS = ['difficulty', 'surface', 'direction', 'tags']
    BOOLEAN_PARAMS = ['is_transport_availability']
    FILTER_PARAMS = NUMERIC_PARAMS + CHOICE_PARAMS + BOOLEAN_PARAMS
  

    def __str__(self):
        """
        String for representing the Model object.
        """
        distance = str(self.distance)
        if (self.distance_max > 0):
            distance += f' - {self.distance_max}'
        return f'{self.title} ({distance} km)'

    def get_absolute_url(self):
        """
        Returns the url to access a particular rout instance.
        """
        return reverse('rout-detail', args=[str(self.id)])

    def display_tags(self):
        """
        Creates a string for the tags. This is required to display tags in Admin.
        """
        return ', '.join([tag.name for tag in self.tags.all()])

    @classmethod
    def get_filtered_routes(cls, **kw):
        """
        Returns queryset of routes, filtered by params
        """
        return cls.objects.filter(
            (Q(distance__range=(kw['min_distance'], kw['max_distance'])) | Q(distance_max__range=(kw['min_distance'], kw['max_distance']))) &
            Q(difficulty__in=kw['difficulty']) &
            Q(surface__in=kw['surface']) &
            Q(direction__in=kw['direction']) &
            Q(tags__in=kw['tags']) &
            Q(is_transport_availability__in=kw['is_transport_availability'])
        ).distinct()

    @classmethod
    def get_distance_range(cls):
        distance_range = cls.objects.aggregate(Min('distance'), Max('distance'), Max('distance_max'))
        min_0 = distance_range['distance__min'] or 0
        max_0 = distance_range['distance__max'] or 0
        max_1 = distance_range['distance_max__max'] or 0
        return Bunch(dict(min_distance=max(1, min_0), max_distance=max(max_0, max_1)))

    @classmethod
    def get_valid_choices(cls, param):
        """
        Returns queryset of routes, filtered by params
        """
        if param not in cls.CHOICE_PARAMS:
            raise Exception(f'param is expected to be on of {cls.CHOICE_PARAMS}')
        model = dict(difficulty=Difficulty, surface=Surface, direction=Direction, tags=Tag)[param]
        available_choices = [i[0] for i in cls.objects.values_list(param).distinct()]
        search_params = list()
        for choice in model.objects.values_list('id', 'name'):
            if choice[0] in available_choices:
                search_params.append(str(choice[0]))
        return search_params

    @classmethod
    def get_valid_param_value(cls, param, value):
        if param == "min_distance":
            if value != None:
                return max(value, cls.get_distance_range().min_distance)
            else:
                return cls.get_distance_range().min_distance
        elif param == "max_distance":
            if value != None:
                return min(value, cls.get_distance_range().max_distance)
            else:
                return cls.get_distance_range().max_distance
        elif param in cls.CHOICE_PARAMS:
            print(f"choice param {param} == {value}")
            valid_values = cls.get_valid_choices(param)
            if value != None:
                _value = []
                for v in value:
                    if v in valid_values:
                        _value.append(v)
                return _value
            else:
                return valid_values
        elif param in cls.BOOLEAN_PARAMS:
            return value
        else:
            raise Exception(f"param is expected to be on of {cls.FILTER_PARAMS}!")


class RouteCollections(models.Model):
    """
    Model of route collections. Collection is set of ruotes with similar features.
    Contains filter data.
    """
    title = models.CharField(max_length=200, help_text="Название подборки")
    min_distance = models.PositiveIntegerField(help_text="Минимальная длина маршрута")
    max_distance = models.PositiveIntegerField(help_text="Максимальная длина маршрута")
    difficulty = models.ManyToManyField(Difficulty, help_text="Сложность маршрутов")
    surface = models.ManyToManyField(Surface, help_text="Тип покрытия")
    direction = models.ManyToManyField(Direction, help_text="Направление. Маршрут попадет в подборку, если у него совпадает хотя бы одно направление")
    tags = models.ManyToManyField(Tag, help_text="Особенности. Маршрут попадет в подборку, если у него совпадает хотя бы одна особенность")
    is_transport_availability = models.ForeignKey(Availability, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='uploads/', null=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_params(self):
        """
        returns http request parameters
        """
        return dumps(dict(
            min_distance=self.min_distance,
            max_distance=self.max_distance,
            difficulty=[str(value.id) for value in self.difficulty.all()],
            surface=[str(value.id) for value in self.surface.all()],
            direction=[str(value.id) for value in self.direction.all()],
            tags=[str(value.id) for value in self.tags.all()],
            is_transport_availability=str(self.is_transport_availability)
        ))


class Gallery(models.Model):
    image = models.ImageField(upload_to='uploads/')
    rout = models.ForeignKey(Rout, on_delete=models.CASCADE, related_name='images')