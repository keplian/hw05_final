import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from posts.forms import PostForm
from posts.models import Group, Post
from posts.tests.constants import DATA_FOR_FORM, URLS

User = get_user_model()


class TestForm(TestCase):
    fixtures = ["fixtures"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.group = Group.objects.get(id=1)
        cls.user = User.objects.get(id=1)
        cls.form = PostForm()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(TestForm.user)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_labels(self):
        """Is form have expected labels"""
        labels = {
            "group": "Выбeрите группу из списка",
            "text": "Напишите о чем ваш пост",
        }
        for value, expected in labels.items():
            with self.subTest(value=value):
                self.assertEqual(TestForm.form[value].label, expected)

    def test_create_new_post_form(self):
        """Correct save post in db and redirect to index"""
        count_posts = Post.objects.count()
        response = TestForm.authorized_client.post(
            URLS["new_post"]["url"], data=DATA_FOR_FORM, follow=True
        )
        self.assertRedirects(response, URLS["index"]["url"])
        self.assertEqual(Post.objects.count(), count_posts + 1)

    def test_edit_post_page_changes_correct(self):
        """Test edited text and new group correctly saves in edited post"""

        form_data = {
            "text": "Edited text",
            "group": 2,
        }
        TestForm.authorized_client.post(
            URLS["post_edit"]["url"], data=form_data, follow=True
        )
        post = Post.objects.get(id=1)
        self.assertEqual((post.text, post.group.id), ("Edited text", 2))
