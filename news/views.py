from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator

from .models import Post

@ensure_csrf_cookie
def index(request):
    """Display the news"""

    # Number of posts per page that will be displayed.
    POSTS_PER_PAGE = 3

    paginator = Paginator(Post.objects.all(), POSTS_PER_PAGE)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    context = {
        "posts": posts,
        "display_shopping_cart": True
    }

    return render(request, "news/index.html", context)


def display_post(request, id):
    """Display post with selected id"""

    context = {
        "post": get_object_or_404(Post, pk=id),
        "display_shopping_cart": True
    }

    return render(request, "news/post.html", context)
