from django.db import models
from django.urls import reverse
from django.db.models import Count, Q, Min, Max


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

    def get_id(self):
        """
        Id of object.
        """
        return self.id


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

    def get_id(self):
        """
        Id of object.
        """
        return self.id


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

    def get_id(self):
        """
        Id of object.
        """
        return self.id


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

    def get_id(self):
        """
        Id of object.
        """
        return self.id


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
    def get_filtered_routes(cls, min_distance, max_distance, difficulties, surfaces, directions, tags, is_transport_availabilities):
        """
        Returns queryset of routes, filtered by params
        """
        return cls.objects.filter(
            (Q(distance__range=(min_distance, max_distance)) | Q(distance_max__range=(min_distance, max_distance))) &
            Q(difficulty__in=difficulties) &
            Q(surface__in=surfaces) &
            Q(direction__in=directions) &
            Q(tags__in=tags) &
            Q(is_transport_availability__in=is_transport_availabilities)
        ).distinct()

    @classmethod
    def get_available_choices(cls, param):
        if param not in ['difficulty', 'surface', 'direction', 'tags']:
            raise Exception('Not multiple choice or exsisting field!')
        model = dict(difficulty=Difficulty, surface=Surface, direction=Direction, tags=Tag)[param]
        available_choices = [i[0] for i in cls.objects.values_list(param).distinct()]
        search_params = list()
        for choice in model.objects.values_list('id', 'name'):
            if choice[0] in available_choices:
                search_params.append(str(choice[0]))
        return search_params


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

    def get_url_params(self):
        """
        returns http request parameters
        """
        params = list()

        params.append(f'min_distance={str(self.min_distance)}')
        params.append(f'max_distance={str(self.max_distance)}')

        param_names = ['difficulty', 'surface', 'direction', 'tags']
        field_names = [self.difficulty, self.surface, self.direction, self.tags]
        for param, field in zip(param_names, field_names):
            values = ''.join([str(value.get_id()) for value in field.all()])
            params.append(f'{param}={values}')

        params.append(f'is_transport_availability={self.is_transport_availability}')

        params_str = '&'.join(params)
        return f'?{params_str}'


class Gallery(models.Model):
    image = models.ImageField(upload_to='uploads/')
    rout = models.ForeignKey(Rout, on_delete=models.CASCADE, related_name='images')