from django.test import TestCase

from ..models import Movie, Comment


# Create your tests here.


class MovieModelTest(TestCase):
    """
    Test module for Movie model
    """

    def setUp(self) -> None:
        Movie.objects.create(Title="Old Boys")

    def test_movie_title(self):
        movie = Movie.objects.get(Title='Old Boys')
        self.assertEqual(movie.Title, "Old Boys")


class CommentModelTest(TestCase):
    """
    Test module for Comment model
    """

    def setUp(self) -> None:
        movie = Movie.objects.create(Title="Old Boys")
        Comment.objects.create(movie_id=movie, movie_comment="Cool movie")

    def test_comment(self):
        comment = Comment.objects.get(movie_comment='Cool movie')
        self.assertEqual(comment.id, 1)
        self.assertEqual(comment.movie_comment, 'Cool movie')
