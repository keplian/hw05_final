from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatechars
from django.test import TestCase

from posts.forms import PostForm
from posts.models import Group, Post
from posts.tests.constants import (DATA_FOR_FORM, FIELD_HELP_TEXTES,
                                   MODEL_FIELD_VERBOSES)

User = get_user_model()


class TestNewPost(TestCase):
    fixtures = ["fixtures"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.group = Group.objects.get(pk=1)
        cls.post = Post.objects.get(pk=1)

    def test_verbose_names(self):
        """Verbose_name in fields has expected value."""
        for value, expected in MODEL_FIELD_VERBOSES.items():
            with self.subTest(value=value):
                name = TestNewPost.post._meta.get_field(value).verbose_name
                self.assertEqual(name, expected)

    def test_help_text(self):
        """Help_text in fields are expected.

        Create new form, not a model cause
        in form Meta is ovverided help_text
        """
        form = PostForm(data=DATA_FOR_FORM)
        for value, expected in FIELD_HELP_TEXTES.items():
            with self.subTest(value=value):
                self.assertEqual(form.fields[value].help_text, expected)

    def test_group_str(self):
        """Test __str__ for expected values."""
        group = TestNewPost.group
        post = TestNewPost.post
        expected_group_name = group.title
        expected_post_name = (
            f"Post from {post.author}, "
            f"published {post.pub_date.date()},"
            f"Text: {truncatechars(post.text, 15)}"
        )
        objects = {
            "group": (group, expected_group_name),
            "post": (post, expected_post_name),
        }
        for value, expected in objects.items():
            with self.subTest(value=value):
                self.assertEqual(expected[1], str(expected[0]))
