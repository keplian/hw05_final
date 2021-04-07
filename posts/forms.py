from django import forms
from django.forms.widgets import Textarea
from django.utils.translation import gettext_lazy as _

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Form based on Post model for create new post in blog."""

    class Meta:
        model = Post
        fields = ("text", "group", "image")
        labels = {
            "text": _("Напишите о чем ваш пост"),
            "group": _("Выбeрите группу из списка"),
            "image": _("Можете загрузить картинку"),
        }
        widgets = {"text": Textarea(attrs={"placeholder": "Введите текст"})}
        help_texts = {
            "text": _("Обязательно к заполнению"),
            "group": _("Необходимо выбрать из списка, или оставить пустым"),
        }


class CommentForm(forms.ModelForm):
    """Form based on Comment model for create comment for post."""

    class Meta:
        model = Comment
        fields = {"text"}
        labels = {"text": _("Напишите ваш комментарий")}
        widgets = {
            "text": Textarea(attrs={"placeholder": "Напишите комментарий"})
        }
        help_texts = {"text": _("Обязательно к заполнению")}
