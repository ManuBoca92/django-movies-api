from django.contrib import admin
from .models import Movie, Comment, MovieDetail, Rating


admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(MovieDetail)
admin.site.register(Rating)