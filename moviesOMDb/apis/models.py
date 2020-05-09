from django.db import models
from django.utils import timezone


class Movie(models.Model):
    """
    Movie model which stores movie tile and created date
    """
    Title = models.CharField(max_length=255)
    Created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return f'Movie: {self.Title} created at {self.Created_at}'


class Comment(models.Model):
    """
    Comment model which stores comments on movie
    """
    movie_id = models.ForeignKey('Movie', related_name='movie',
                                 on_delete=models.CASCADE)
    movie_comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment: {self.movie_comment} was created at {self.created_at}'


class MovieDetail(models.Model):
    """
    Store movie details
    """
    Title = models.CharField(max_length=100)
    Year = models.CharField(max_length=100)
    Rated = models.CharField(max_length=100)
    Released = models.CharField(max_length=100)
    Runtime = models.CharField(max_length=100)
    Genre = models.CharField(max_length=100)
    Director = models.CharField(max_length=100)
    Writer = models.CharField(max_length=1000)
    Actors = models.CharField(max_length=1000)
    Plot = models.CharField(max_length=1000)
    Language = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    Awards = models.CharField(max_length=100)
    Poster = models.CharField(max_length=1000)
    Metascore = models.CharField(max_length=100)
    imdbRating = models.CharField(max_length=100)
    imdbVotes = models.CharField(max_length=100)
    imdbID = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    DVD = models.CharField(max_length=100)
    BoxOffice = models.CharField(max_length=100)
    Production = models.CharField(max_length=100)
    Website = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.Title}'


class Rating(models.Model):
    """
    Stores movie ratings and is related to Movie detail model
    """
    Source = models.CharField(max_length=100)
    Value = models.CharField(max_length=100)
    movie_detail = models.ForeignKey(MovieDetail,
                                     on_delete=models.CASCADE,
                                     related_name="Ratings")

    def __str__(self):
        return f'Ratings from {self.Source} for {self.movie_detail})'
