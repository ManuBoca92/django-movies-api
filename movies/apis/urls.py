from django.conf.urls import url
from rest_framework import routers

from .views import CommentsViewSet, MoviesViewSet, MovieDetailsView, TopView

router = routers.DefaultRouter()
router.register(r'movies', MoviesViewSet, basename='movies_view')
router.register(r'comments', CommentsViewSet, basename='comments_view')

urlpatterns = [
    url(r'movie-detail', MovieDetailsView.as_view(), name='movie_details_view'),
    url(r'top', TopView.as_view(), name='top_view')
]

urlpatterns += router.urls
