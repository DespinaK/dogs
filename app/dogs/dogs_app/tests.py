from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post, Location
from .forms import PostForm
from django.shortcuts import redirect

class TestEntriesView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('entries')  # replace 'entries' with the actual URL name

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_request_with_valid_data(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'title': 'Test Post',
            'content': 'Test content',
            'image': image,
            'lat': '40.7128',
            'lon': '74.0060'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect status code
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Location.objects.count(), 0)  # Location model is not used in the view

    def test_post_request_with_invalid_lat_lon(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'title': 'Test Post',
            'content': 'Test content',
            'image': image,
            'lat': 'invalid_lat',
            'lon': 'invalid_lon'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)  # bad request status code
        self.assertEqual(Post.objects.count(), 0)

    def test_post_request_with_missing_lat_lon(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'title': 'Test Post',
            'content': 'Test content',
            'image': image
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)  # bad request status code
        self.assertEqual(Post.objects.count(), 0)