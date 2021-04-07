from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from posts.forms import CommentForm, PostForm

from .models import Group, Post

User = get_user_model()


def index(request):
    """Show latest 10 posts in main page sorted desc."""
    latest = Post.objects.all()
    paginator = Paginator(latest, settings.PER_PAGE_INDEX)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page})


def group_posts(request, slug):
    """Show last 12 posts in desc sort by selected group."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all()
    paginator = Paginator(posts, settings.PER_PAGE_GROUP)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page})


@login_required
def new_post(request):
    """Create form for new post and save post in db."""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "new_post.html", {"form": form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = user.posts.all()
    paginator = Paginator(user_posts, settings.PER_PAGE_GROUP)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"author": user, "page": page})


def post_view(request, username, post_id):
    "Show post for specified author username and post id"
    form = CommentForm()
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    return render(
        request,
        "post.html",
        {"author": user, "post": post, "comments": comments, "form": form},
    )


@login_required()
def post_edit(request, username, post_id):
    "Edit existing post, if user not a post's author - redirect to post page"
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect("post", username=username, post_id=post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(
                "post", username=request.user.username, post_id=post_id
            )
    return render(request, "new_post.html", {"form": form, "edit": True})


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def create_comment(request, username, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    return render(request, "comments.html", {"form": form})


@login_required
def add_comment(request, post_id, username):
    form = CommentForm(request.POST)
    if form.is_valid():
        post = get_object_or_404(Post, id=post_id)
        author = get_object_or_404(User, username=username)
        value = form.save(commit=False)
        value.post = post
        value.author = author
        value.save()
        return redirect("post", username, post_id)
