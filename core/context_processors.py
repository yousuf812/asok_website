from .models import OrganizationInfo


def organization_info(request):
    organization = OrganizationInfo.objects.first()

    return {
        "organization": organization,
    }