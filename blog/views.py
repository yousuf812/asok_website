from django.shortcuts import get_object_or_404, render

from .models import BlogCategory, BlogPost
from django.core.paginator import Paginator
from django.urls import reverse


def blog_list(request):

    selected_category = request.GET.get("category")

    posts = BlogPost.objects.filter(
        status="published"
    ).select_related("category")

    categories = BlogCategory.objects.filter(
        is_active=True
    )

    if selected_category:
        posts = posts.filter(
            category__slug=selected_category
        )

    paginator = Paginator(posts, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "posts": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "selected_category": selected_category,
    }

    return render(
        request,
        "blog/list.html",
        context
    )


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.select_related("category"),
        slug=slug,
        status="published",
    )

    post.views += 1
    post.save(update_fields=["views"])

    context = {
    "post": post,
    "breadcrumb_items": [
        {
            "name": "Blog",
            "url": reverse("blog:list"),
        },
        {
            "name": post.title,
            "url": reverse(
                "blog:detail",
                kwargs={"slug": post.slug},
            ),
        },
    ],
}

    return render(
        request,
        "blog/detail.html",
        context
    )