from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Max

from .models import Post


class PostsTestCase(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username="Test", password="testing123")
        test_post_one = Post.objects.create(
            title="Test Post 1",
            content="Some text here.",
            author=test_user
            )
        test_Post_two = Post.objects.create(
            title="Test Post 2",
            content="More text here.",
            author=test_user
        )


    def test_view_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 2)


    def test_view_post(self):
        response = self.client.get("/post/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["post"].title, "Test Post 1")


    def test_view_incorrect_post_id(self):
        max_id = Post.objects.all().aggregate(Max("id"))["id__max"]
        response = self.client.get(f"/post/{max_id + 1}")
        self.assertEqual(response.status_code, 404)
