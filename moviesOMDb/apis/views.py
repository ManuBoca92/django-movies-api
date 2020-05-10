import datetime

from django.conf import settings
from django.db.models import Count, Window, F
from django.db.models.functions.window import DenseRank
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .models import Movie, Comment, MovieDetail
from .serializers import MovieSerializer, CommentSerializer, \
    MovieDetailSerializer
from .views_helpers import call_external_api

OMDB_API_KEY = settings.OMDB_API_KEY


def index(request):
    html = '<h3>Welcome! Use API endpoints to make requests for movies or ' \
           'comments</h3>'
    return HttpResponse(html)


class MoviesViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Movie instances.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_fields = ['id', 'Title', 'Created_at']
    ordering_fields = '__all__'
    search_fields = ['id', 'Title', 'Created_at']

    def create(self, request, *args, **kwargs):
        serializers = [MovieSerializer, MovieDetailSerializer]
        if 'Title' in request.data:
            title = request.data['Title']
            url = f'http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}'
            data = call_external_api(url)
            if data['Response'] == 'True':
                if not Movie.objects.filter(Title=data['Title']).exists():
                    for serializer in serializers:
                        s = serializer(data=data)
                        s.is_valid(raise_exception=True)
                        s.save()
                    return Response(s.data, status=status.HTTP_201_CREATED)
                return Response(data={'Error message': 'Movie already exists!'})
            return Response(data={'Error message': 'Not such movie was found!'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(
            data={
                'Error message': 'Please provide a "Title" in POST request body'},
            status=status.HTTP_400_BAD_REQUEST)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Movie instances.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_fields = ['created_at', 'id', 'movie_comment', 'movie_id__id']
    ordering_fields = '__all__'
    search_fields = ['created_at', 'id', 'movie_comment', 'movie_id__id']

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie_id')
        movie_comment = request.data.get('movie_comment')

        if not (movie_id and movie_comment):
            return Response(
                data={"Error message": 'Please provide request POST body'},
                status=status.HTTP_400_BAD_REQUEST)

        if Movie.objects.filter(id=movie_id).exists():
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data={'Error message': f'movie id {movie_id} does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )


class MovieDetailsView(views.APIView):
    """
    An APIViwe to list all movies details
    """

    def get(self, request, format=None):
        movie_details = MovieDetail.objects.all()
        serializer = MovieDetailSerializer(movie_details, many=True)
        return Response(serializer.data)


class TopView(views.APIView):
    """
    List rankings of movies according to number of comments
    """

    def get(self, request, format=None):
        dense_rank = Window(
            expression=DenseRank(),
            order_by=F('total_comments').desc()
        )

        start_date = datetime.date(2020, 4, 13)
        end_date = datetime.datetime.now()
        ranking = (Comment.objects
                   .filter(created_at__range=(start_date, end_date))
                   .values('movie_id')
                   .annotate(total_comments=Count('movie_comment'))
                   .annotate(rank=dense_rank))
        return Response(ranking)
