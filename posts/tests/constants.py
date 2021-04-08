from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Page
from django.urls.base import reverse
from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()

small_gif = (
    b"\x47\x49\x46\x38\x39\x61\x02\x00"
    b"\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
    b"\x00\x00\x00\x2C\x00\x00\x00\x00"
    b"\x02\x00\x01\x00\x00\x02\x02\x0C"
    b"\x0A\x00\x3B"
)
UPLOADED_IMAGE = SimpleUploadedFile(
    name="small.gif", content=small_gif, content_type="image/gif"
)

URLS = {
    "index": {
        "template": "index.html",
        "url": reverse("index"),
        "context": {"page": Page},
    },
    "group_posts": {
        "template": "group.html",
        "url": reverse("group_posts", kwargs={"slug": "test-slug"}),
        "context": {"page": Page, "group": Group},
    },
    "new_post": {
        "template": "new_post.html",
        "url": reverse("new_post"),
        "context": {"form": PostForm},
    },
    "post_edit": {
        "template": "new_post.html",
        "url": reverse("post_edit", kwargs={"username": "leo", "post_id": 1}),
        "context": {"form": PostForm, "edit": bool},
    },
    "profile": {
        "template": "profile.html",
        "url": reverse("profile", kwargs={"username": "leo"}),
        "context": {"author": User, "page": Page},
    },
    "post_view": {
        "template": "post.html",
        "url": reverse("post", kwargs={"username": "leo", "post_id": 1}),
        "context": {"author": User, "post": Post},
    },
    "follow_index": {
        "template": "follow.html",
        "url": reverse("follow_index"),
        "context": {"page": Page},
    },
    "profile_follow": {
        "template": "",
        "url": reverse("profile_follow", kwargs={"username": "keplian"}),
        "context": {},
    },
    "profile_unfollow": {
        "template": "",
        "url": reverse("profile_unfollow", kwargs={"username": "keplian"}),
        "context": {},
    },
    "add_comment": {
        "template": "",
        "url": reverse(
            "add_comment", kwargs={"username": "leo", "post_id": 1}
        ),
        "context": {},
    },
}

DATA_FOR_FORM = {"text": "Form test text", "group": 1, "image": UPLOADED_IMAGE}


MODEL_FIELD_VERBOSES = {"text": "Текст поста", "group": "post's group"}

FIELD_HELP_TEXTES = {
    "group": "Необходимо выбрать из списка, или оставить пустым",
    "text": "Обязательно к заполнению",
}
