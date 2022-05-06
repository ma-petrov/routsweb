from django.db import models
from django.urls import reverse


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
    distance = models.PositiveIntegerField(help_text="Enter distance in kilometers")
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)
    surface = models.ForeignKey(Surface, on_delete=models.SET_NULL, null=True)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, help_text="Select characteristics")
    description = models.CharField(max_length=1000)
    goggle_map_link = models.CharField(max_length=200)
    bike_map_link = models.CharField(max_length=200)
    kml_file_link = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.title} ({self.distance} km)'

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
