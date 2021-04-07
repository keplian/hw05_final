from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.urls = {
            "about/author.html": "/about/author/",
            "about/tech.html": "/about/tech/",
        }

    def test_about_url_exists_at_desired_location(self):
        """Test avaliable 'about' urls."""
        for url in self.urls.values():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_about_url_uses_correct_template(self):
        """Test correct templates for 'about' urls """
        for template, url in self.urls.items():
            with self.subTest(url=url, template=template):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
