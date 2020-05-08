from rest_framework import routers
from django.conf.urls import url
from apis import views

router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'top', views.TopViewSet)