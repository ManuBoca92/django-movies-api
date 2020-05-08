from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Movie, Comment, MovieDetail, Rating


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('Source', 'Value')
        read_only_fields = ('movie',)


class MovieDetailSerializer(WritableNestedModelSerializer):
    Ratings = RatingSerializer(many=True)

    class Meta:
        model = MovieDetail
        fields = '__all__'
