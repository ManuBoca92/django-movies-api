from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import Movie


class MovieApiTest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('apis:movie-list')

    def test_get_empty_movie_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_post_movie_title(self):
        data = {'Title': 'Die Another Day'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_two_movies(self):
        self.client.post(self.url, {'Title': 'Die Another Day'}, format='json')
        self.client.post(self.url, {'Title': 'Good Friday'}, format='json')
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 2)

    def test_post_movie_request_no_body(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {
                             'Error message': 'Please provide a "Title" in POST request body'})

    def test_post_request_existing_movie(self):
        data = {'Title': 'Good'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.json(),
                         {'Error message': 'Movie already exists!'})

    def test_post_request_movie_not_found(self):
        data = {'Title': 'g2rwe214ds'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentApiTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('apis:comment-list')

    def test_get_empty_comment_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_post_comment_to_movie_that_exist(self):
        Movie.objects.create(Title="Old Boys")
        data = {'movie_id': '1', 'movie_comment': 'Nice movie'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_comment_to_movie_that_does_not_exist(self):
        data = {'movie_id': '1', 'movie_comment': 'Nice movie'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_two_comments(self):
        Movie.objects.create(Title="Old Boys")
        self.client.post(
            self.url,
            {'movie_id': '1', 'movie_comment': 'Nice movie'},
            format='json')
        self.client.post(
            self.url,
            {'movie_id': '1', 'movie_comment': 'Nice movie'},
            format='json')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
