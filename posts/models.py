from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import truncatechars

User = get_user_model()


class Group(models.Model):
    """Model of groups all posts.

    Fields:
        title [CharField]: name of group, max 200 symbols
        slug [SlugField]: slug of path, must be unique
        description [TextField]: text about group
    """

    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Описание группы")

    class Meta:
        verbose_name = "Group"

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Model for posts user writed.

    Fields:
        text [TextField]: post text
        pub_date [DateTimeField]: date in post was published
        author [ForeignKey(User)]: user writed posts
        group [ForeignKey(Group)]: group posts
        image [ImageFiel]: image


    Posts default ordering by desc pub_date field
    """

    text = models.TextField("Текст поста")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="post's author",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="group_posts",
        verbose_name="post's group",
    )
    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Post"

    def __str__(self) -> str:
        return (
            f"Post from {self.author}, "
            f"published {self.pub_date.date()},"
            f"Text: {truncatechars(self.text, 15)}"
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Post comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="User comments",
    )
    text = models.TextField("Comment's text")
    created = models.DateTimeField("Date post was created", auto_now_add=True)
