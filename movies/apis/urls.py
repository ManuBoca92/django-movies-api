from django.conf.urls import url

from .views import CommentsViewSet, MoviesViewSet, MovieDetailsView, TopView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'movies', MoviesViewSet, basename='movies_view')
router.register(r'comments', CommentsViewSet, basename='comments_view')

urlpatterns = [
    # url(r'movies', MoviesView.as_view(), name='movies_view'),
    # url(r'comments', CommentsView.as_view(), name='comments_view'),
    url(r'movie-detail', MovieDetailsView.as_view(), name='movie_details_view'),
    url(r'top', TopView.as_view(), name='top_view')
]

urlpatterns += router.urls
