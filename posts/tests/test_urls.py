# posts/tests/test_urls.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        _group = Group.objects.create(
            title="Тестовая",
            slug="test-slug",
            description="Тестовое описание",
        )
        cls.user = User.objects.create(username="Test_user")
        cls.wrong_user = User.objects.create(username="Wrong_user")
        cls.post = Post.objects.create(
            text="Test post", group=_group, author=StaticURLTests.user
        )
        cls.url_public_names = {
            "index.html": "/",
            "group.html": "/group/test-slug/",
            "post.html": (
                f"/{StaticURLTests.user.username}/{StaticURLTests.post.id}/"
            ),
            "about/author.html": "/about/author/",
            "about/tech.html": "/about/tech/",
            "profile.html": f"/{StaticURLTests.user.username}/",
        }
        cls.url_private_names = {
            "new_post.html": "/new/",
        }
        cls.all_urls = {**cls.url_private_names, **cls.url_public_names}
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(StaticURLTests.user)

    def test_guest_pages(self):
        """Check all pages are aviable for anonymous user."""
        for url in StaticURLTests.url_public_names.values():
            with self.subTest(url=url):
                response = StaticURLTests.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_pages_for_authorized(self):
        """Check private pages are aviable only for authorized user."""
        for url in StaticURLTests.url_private_names.values():
            with self.subTest(url=url):
                response = StaticURLTests.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_redirect_anonymous(self):
        """Private pages should redirect to login page."""
        for url in StaticURLTests.url_private_names.values():
            with self.subTest(url=url):
                response = StaticURLTests.guest_client.get(url)
                self.assertEqual(response.status_code, 302)

    def test_url_uses_correct_template(self):
        """All urls uses appropriate template."""
        for template, url in StaticURLTests.all_urls.items():
            with self.subTest(url=url, template=template):
                response = StaticURLTests.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_edit_post_page_for_all_types_users(self):
        """Test edit post page available for author,
        and redirect others to post page.
        """
        url = (
            f"/{StaticURLTests.user.username}/"
            f"{StaticURLTests.post.id}/edit/"
        )
        wrong_client = Client()
        wrong_client.force_login(StaticURLTests.wrong_user)
        response = StaticURLTests.authorized_client.get(url)
        self.assertEqual(response.status_code, 200)
        response = StaticURLTests.guest_client.get(url)
        self.assertEqual(response.status_code, 302)
        response = wrong_client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_edit_post_page_uses_correct_template(self):
        """Edit post page uses new_post.html template."""
        url = (
            f"/{StaticURLTests.user.username}/"
            f"{StaticURLTests.post.id}/edit/"
        )
        response = StaticURLTests.authorized_client.get(url)
        self.assertTemplateUsed(response, "new_post.html")

    def test_edit_post_page_redirects_wrong_user(self):
        """Test redirect not author post from edit post page to post page."""
        wrong_client = Client()
        wrong_client.force_login(StaticURLTests.wrong_user)
        url = (
            f"/{StaticURLTests.user.username}/"
            f"{StaticURLTests.post.id}/edit/"
        )
        redirect_url = (
            f"/{StaticURLTests.user.username}/" f"{StaticURLTests.post.id}/"
        )
        response = wrong_client.get(url)
        self.assertRedirects(response, redirect_url)

    def test_wrong_page_get_404(self):
        """Return 404 code on wrong url."""
        response = StaticURLTests.guest_client.get("/abracadabra/")
        self.assertEqual(response.status_code, 404)
