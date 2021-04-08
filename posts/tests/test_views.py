from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls.base import reverse

from posts.models import Follow, Group, Post
from posts.tests.constants import URLS

User = get_user_model()


class PostPagesTests(TestCase):
    fixtures = ["fixtures"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.get(id=1)

        cls.user = User.objects.get(id=1)

        cls.wrong_group = Group.objects.get(id=2)

        test_posts_list = (
            Post(group=cls.group, author=cls.user, text=f"Test post N{i}")
            for i in range(14)
        )
        Post.objects.bulk_create(test_posts_list)
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(PostPagesTests.user)

    def test_pages_uses_correct_template(self):
        """Testing pages in URLS use correct templates."""
        for values in URLS.values():
            if values["template"]:
                with self.subTest(url=values["url"]):
                    response = PostPagesTests.authorized_client.get(
                        values["url"]
                    )
                    self.assertTemplateUsed(response, values["template"])

    def test_home_page_has_correct_amount_posts(self):
        """Index page shows no more than 10 posts."""
        response = self.authorized_client.get(URLS["index"]["url"])
        self.assertEqual(
            len(response.context.get("page").object_list),
            settings.PER_PAGE_INDEX,
        )

    def test_group_page_has_correct_amount_posts(self):
        """Group page shows no more than 12 posts."""
        response = self.authorized_client.get(URLS["group_posts"]["url"])
        self.assertEqual(
            len(response.context.get("page").object_list),
            settings.PER_PAGE_GROUP,
        )

    def test_pages_have_correct_context(self):
        """Pages has Post object in context."""
        for item, values in URLS.items():
            with self.subTest(url=values["url"]):
                response = PostPagesTests.authorized_client.get(values["url"])
                for context, context_object in values["context"].items():
                    if context_object:
                        self.assertIsInstance(
                            response.context.get(context), context_object
                        )

    def test_new_page_has_fields_in_form(self):
        """New post form has expected fields."""
        response = PostPagesTests.authorized_client.get(
            URLS["new_post"]["url"]
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.ChoiceField,
            "image": forms.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields[value]
                self.assertIsInstance(form_field, expected)

    def test_is_post_in_group_and_home_pages(self):
        """Does test have post in group and index pages"""

        test_post = Post.objects.get(id=1)

        for value in URLS:
            if value in ("index", "group_posts"):
                with self.subTest(url=URLS[value]["url"]):
                    response = PostPagesTests.guest_client.get(
                        URLS[value]["url"]
                    )
                    self.assertIn(
                        test_post,
                        response.context.get("page").paginator.object_list,
                    )

    def test_post_in_correct_group(self):
        """Created new post is only in his own group page."""
        test_post = Post.objects.get(id=1)
        wrong_group_url = reverse("group_posts", kwargs={"slug": "wrong-slug"})
        response = PostPagesTests.authorized_client.get(wrong_group_url)
        self.assertNotIn(test_post, response.context.get("page"))

    def test_cache_is_working_on_index_page(self):
        """Cache 20 sec on index page for posts"""
        response = PostPagesTests.guest_client.get(URLS["index"]["url"])
        content_response_before = response.content
        Post.objects.create(text="test_cache", author=PostPagesTests.user)
        response = PostPagesTests.guest_client.get(URLS["index"]["url"])
        content_after = response.content
        self.assertEqual(content_response_before, content_after)
        cache.clear()
        response = PostPagesTests.guest_client.get(URLS["index"]["url"])
        lenght_response_after_sleep = response.content
        self.assertNotEqual(
            content_response_before, lenght_response_after_sleep
        )

    def test_follower_can_follow_and_unfollow(self):
        """User can follow and unfollow author.

        Posts by followed author appear in user's follow index page
        and don't appear in wrong user's follow index page
        """
        keplian = User.objects.get(pk=4)
        new_user = User.objects.create_user("New follower")
        new_follower = Client()
        new_follower.force_login(new_user)
        follow_exists = False
        PostPagesTests.authorized_client.get(URLS["profile_follow"]["url"])
        follow_exists = Follow.objects.filter(
            user=PostPagesTests.user, author=keplian
        ).first()
        self.assertIsNotNone(follow_exists)
        response_new_follower_follow_index = new_follower.get(
            URLS["follow_index"]["url"]
        )
        response_test_user_follow_index = PostPagesTests.authorized_client.get(
            URLS["follow_index"]["url"]
        )
        self.assertIn(
            Post.objects.get(pk=2),
            response_test_user_follow_index.context.get("page"),
        )
        self.assertNotIn(
            Post.objects.get(pk=2),
            response_new_follower_follow_index.context.get("page"),
        )
        PostPagesTests.authorized_client.get(URLS["profile_unfollow"]["url"])
        follow_exists = Follow.objects.filter(
            user=PostPagesTests.user, author=keplian
        ).exists()
        self.assertFalse(follow_exists)
