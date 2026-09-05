from django.shortcuts import get_object_or_404, render

from .models import GalleryCategory, GalleryImage
from django.urls import reverse


def gallery_list(request):

    selected_category = request.GET.get("category")

    images = GalleryImage.objects.filter(
        is_active=True
    ).select_related(
        "category"
    )

    categories = GalleryCategory.objects.filter(
        is_active=True
    )

    if selected_category:
        images = images.filter(
            category__slug=selected_category
        )

    context = {
    "image": image,
    "breadcrumb_items": [
        {
            "name": "Gallery",
            "url": reverse("gallery:list"),
        },
        {
            "name": image.title,
            "url": reverse(
                "gallery:detail",
                kwargs={"slug": image.slug},
            ),
        },
    ],
}

    return render(
        request,
        "gallery/list.html",
        context
    )


def gallery_detail(request, slug):

    image = get_object_or_404(
        GalleryImage.objects.select_related("category"),
        slug=slug,
        is_active=True,
    )

    return render(
        request,
        "gallery/detail.html",
        {"image": image}
    )