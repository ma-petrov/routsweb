from django.contrib import admin
from .models import Rout, Difficulty, Surface, Direction, Tag, RouteCollections, Availability, Gallery, UserBehaviourData

admin.site.register(Difficulty)
admin.site.register(Surface)
admin.site.register(Direction)
admin.site.register(Tag)
admin.site.register(RouteCollections)
admin.site.register(Availability)
admin.site.register(UserBehaviourData)

class GalleryInline(admin.TabularInline):
    model = Gallery

@admin.register(Rout)
class RoutAdmin(admin.ModelAdmin):
    inlines = [GalleryInline]
