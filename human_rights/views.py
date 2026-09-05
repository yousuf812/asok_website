from django.shortcuts import render, get_object_or_404

from .models import (
    HumanRightsCategory,
    HumanRightsArticle,
    HumanRightsFAQ,
)
from django.urls import reverse


def human_rights_home(request):

    categories = HumanRightsCategory.objects.filter(
        is_active=True
    )

    articles = HumanRightsArticle.objects.filter(
        is_active=True
    ).select_related(
        "category"
    )

    featured_articles = articles.filter(
        is_featured=True
    )

    faqs = HumanRightsFAQ.objects.filter(
        is_active=True
    )

    context = {
        "categories": categories,
        "articles": articles,
        "featured_articles": featured_articles,
        "faqs": faqs,
    }

    return render(
        request,
        "human_rights/home.html",
        context
    )


def human_rights_article(request, slug):

    article = get_object_or_404(
        HumanRightsArticle.objects.select_related(
            "category"
        ),
        slug=slug,
        is_active=True,
    )

    context = {
    "article": article,
    "breadcrumb_items": [
        {
            "name": "Human Rights",
            "url": reverse("human_rights:home"),
        },
        {
            "name": article.title,
            "url": reverse(
                "human_rights:article_detail",
                kwargs={"slug": article.slug},
            ),
        },
    ],
}

    return render(
        request,
        "human_rights/article_detail.html",
        context
    )