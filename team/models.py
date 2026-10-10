from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class TeamMember(models.Model):

    ROLE_CHOICES = [
        ("founder", "Founder"),
        ("director", "Director"),
        ("coordinator", "Coordinator"),
        ("legal_advisor", "Legal Advisor"),
        ("human_rights", "Human Rights Officer"),
        ("member", "Team Member"),
    ]

    name = models.CharField(max_length=150)

    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
    )

    designation = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default="member",
    )

    bio = models.TextField(
        blank=True,
        help_text="Short biography of the team member.",
    )

    photo = models.ImageField(
        upload_to="team/",
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    facebook_url = models.URLField(
        blank=True,
    )

    linkedin_url = models.URLField(
        blank=True,
    )

    website_url = models.URLField(
        blank=True,
    )

    is_featured = models.BooleanField(
        default=False,
        help_text="Show this member in the featured team section.",
    )

    is_active = models.BooleanField(
        default=True,
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Lower number appears first.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_designation_display()}"


# ============================================================
# ASOK COMMITTEE MANAGEMENT
# ============================================================


class CommitteeType(models.TextChoices):
    CENTRAL = "central", "Central Committee"
    DIVISION = "division", "Division Committee"
    DISTRICT = "district", "District Committee"
    METROPOLITAN = "metropolitan", "Metropolitan Committee"
    THANA_UPAZILA = "thana_upazila", "Thana / Upazila Committee"
    MUNICIPALITY = "municipality", "Municipality Committee"
    UNION_WARD = "union_ward", "Union / Ward Committee"


class CommitteeMemberType(models.TextChoices):
    MEMBER = "member", "Committee Member"
    ADVISOR = "advisor", "Advisory Council"




class CommitteeDesignation(models.TextChoices):
    PRESIDENT = "president", "সভাপতি"
    SENIOR_VICE_PRESIDENT = "senior_vice_president", "সিনিয়র সহ-সভাপতি"
    VICE_PRESIDENT = "vice_president", "সহ-সভাপতি"
    GENERAL_SECRETARY = "general_secretary", "সাধারণ সম্পাদক"
    JOINT_GENERAL_SECRETARY = "joint_general_secretary", "যুগ্ম সাধারণ সম্পাদক"
    ORGANIZING_SECRETARY = "organizing_secretary", "সাংগঠনিক সম্পাদক"
    ASSISTANT_ORGANIZING_SECRETARY = (
        "assistant_organizing_secretary",
        "সহ সাংগঠনিক সম্পাদক",
    )
    SONTRO_SECRETARY = "sontro_secretary", "সন্ত্র সম্পাদক"
    ASSISTANT_SONTRO_SECRETARY = (
        "assistant_sontro_secretary",
        "সহ সন্ত্র সম্পাদক",
    )
    PUBLICITY_SECRETARY = "publicity_secretary", "প্রচার সম্পাদক"
    ASSISTANT_PUBLICITY_SECRETARY = (
        "assistant_publicity_secretary",
        "সহ-প্রচার সম্পাদক",
    )
    FINANCE_SECRETARY = "finance_secretary", "অর্থ সম্পাদক"
    RELIGIOUS_AFFAIRS_SECRETARY = (
        "religious_affairs_secretary",
        "ধর্ম বিষয়ক সম্পাদক",
    )
    ASSISTANT_RELIGIOUS_AFFAIRS_SECRETARY = (
        "assistant_religious_affairs_secretary",
        "সহ ধর্ম বিষয়ক সম্পাদক",
    )
    IT_SECRETARY = (
        "it_secretary",
        "তথ্য ও প্রযুক্তি বিষয়ক সম্পাদক",
    )
    ASSISTANT_IT_SECRETARY = (
        "assistant_it_secretary",
        "সহ তথ্য ও প্রযুক্তি বিষয়ক সম্পাদক",
    )
    SOCIAL_WELFARE_SECRETARY = (
        "social_welfare_secretary",
        "সমাজ কল্যাণ বিষয়ক সম্পাদক",
    )
    ASSISTANT_SOCIAL_WELFARE_SECRETARY = (
        "assistant_social_welfare_secretary",
        "সহ সমাজ কল্যাণ বিষয়ক সম্পাদক",
    )
    HUMAN_RIGHTS_SECRETARY = (
        "human_rights_secretary",
        "মানবাধিকার বিষয়ক সম্পাদক",
    )
    ASSISTANT_HUMAN_RIGHTS_SECRETARY = (
        "assistant_human_rights_secretary",
        "সহ মানবাধিকার বিষয়ক সম্পাদক",
    )
    SUPERVISORY_SECRETARY = (
        "supervisory_secretary",
        "তত্ত্বাবধায়ক সম্পাদক",
    )
    ASSISTANT_SUPERVISORY_SECRETARY = (
        "assistant_supervisory_secretary",
        "সহ তত্ত্বাবধায়ক সম্পাদক",
    )
    HOUSING_SECRETARY = (
        "housing_secretary",
        "আবাসন বিষয়ক সম্পাদক",
    )
    ASSISTANT_HOUSING_SECRETARY = (
        "assistant_housing_secretary",
        "সহ আবাসন বিষয়ক সম্পাদক",
    )
    INTERNATIONAL_AFFAIRS_SECRETARY = (
        "international_affairs_secretary",
        "আন্তর্জাতিক বিষয়ক সম্পাদক",
    )
    ASSISTANT_INTERNATIONAL_AFFAIRS_SECRETARY = (
        "assistant_international_affairs_secretary",
        "সহ আন্তর্জাতিক বিষয়ক সম্পাদক",
    )
    RELIEF_REHABILITATION_SECRETARY = (
        "relief_rehabilitation_secretary",
        "ত্রাণ ও পুনর্বাসন বিষয়ক সম্পাদক",
    )
    ASSISTANT_RELIEF_REHABILITATION_SECRETARY = (
        "assistant_relief_rehabilitation_secretary",
        "সহ ত্রাণ ও পুনর্বাসন বিষয়ক সম্পাদক",
    )
    PRESS_PUBLICATION_SECRETARY = (
        "press_publication_secretary",
        "প্রেস ও প্রকাশনা বিষয়ক সম্পাদক",
    )
    ASSISTANT_PRESS_PUBLICATION_SECRETARY = (
        "assistant_press_publication_secretary",
        "সহ প্রেস ও প্রকাশনা বিষয়ক সম্পাদক",
    )
    RECEPTION_SECRETARY = (
        "reception_secretary",
        "আপ্যায়ন বিষয়ক সম্পাদক",
    )
    ASSISTANT_RECEPTION_SECRETARY = (
        "assistant_reception_secretary",
        "সহ আপ্যায়ন বিষয়ক সম্পাদক",
    )
    MEDIA_SECRETARY = "media_secretary", "মিডিয়া বিষয়ক সম্পাদক"
    ASSISTANT_MEDIA_SECRETARY = (
        "assistant_media_secretary",
        "সহ মিডিয়া বিষয়ক সম্পাদক",
    )
    EDUCATION_SECRETARY = "education_secretary", "শিক্ষা বিষয়ক সম্পাদক"
    ASSISTANT_EDUCATION_SECRETARY = (
        "assistant_education_secretary",
        "সহ শিক্ষা বিষয়ক সম্পাদক",
    )
    HEALTH_SECRETARY = "health_secretary", "স্বাস্থ্য বিষয়ক সম্পাদক"
    ASSISTANT_HEALTH_SECRETARY = (
        "assistant_health_secretary",
        "সহ স্বাস্থ্য বিষয়ক সম্পাদক",
    )
    MEDICAL_ACTIVIST = "medical_activist", "চিকিৎসা-অভিনেত্রী"
    SPORTS_SECRETARY = "sports_secretary", "ক্রীড়া বিষয়ক সম্পাদক"
    WOMEN_CHILDREN_SECRETARY = (
        "women_children_secretary",
        "মহিলা ও শিশু বিষয়ক সম্পাদক",
    )
    ASSISTANT_WOMEN_CHILDREN_SECRETARY = (
        "assistant_women_children_secretary",
        "সহ মহিলা ও শিশু বিষয়ক সম্পাদক",
    )
    INTELLECTUAL_SPORTS_SECRETARY = (
        "intellectual_sports_secretary",
        "বুদ্ধ ও ক্রীড়া বিষয়ক সম্পাদক",
    )
    ASSISTANT_INTELLECTUAL_SPORTS_SECRETARY = (
        "assistant_intellectual_sports_secretary",
        "সহ বুদ্ধ ও ক্রীড়া বিষয়ক সম্পাদক",
    )
    EXECUTIVE_MEMBER = "executive_member", "নির্বাহী সদস্য"
    MEMBER = "member", "সদস্য"


class CommitteeMember(models.Model):
    member = models.ForeignKey(
        "membership.Member",
        on_delete=models.CASCADE,
        related_name="committee_positions",
    )

    committee_type = models.CharField(
        max_length=30,
        choices=CommitteeType.choices,
    )

    member_type = models.CharField(
        max_length=20,
        choices=CommitteeMemberType.choices,
        default=CommitteeMemberType.MEMBER,
    )

    designation = models.CharField(
        max_length=60,
        choices=CommitteeDesignation.choices,
        default=CommitteeDesignation.MEMBER,
    )

    # Bangladesh Location
    division = models.ForeignKey(
        "Division",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="committee_members",
    )

    district = models.ForeignKey(
        "District",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="committee_members",
    )

    thana_upazila = models.ForeignKey(
        "Upazila",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="committee_members",
    )

    municipality = models.ForeignKey(
        "Municipality",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="committee_members",
    )

    union_ward = models.ForeignKey(
        "UnionWard",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="committee_members",
    )

    village = models.CharField(
        max_length=150,
        blank=True,
    )

    post_office = models.CharField(
        max_length=150,
        blank=True,
    )

    effective_date = models.DateField()

    is_active = models.BooleanField(
        default=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "committee_type",
            "designation",
            "member__application__full_name",
        ]

        verbose_name = "Committee Member"
        verbose_name_plural = "Committee Members"

    @property
    def effective_status(self):
        """
        Return the member's actual status based on
        the current month's payment.
        """
        if self.status != "active":
            return self.status

        today = timezone.localdate()

        has_paid_current_month = self.application.payments.filter(
            payment_type="monthly",
            status="paid",
            payment_month__year=today.year,
            payment_month__month=today.month,
        ).exists()

        if not has_paid_current_month:
            return "inactive"

        return "active"

    @property
    def effective_status_display(self):
        status_labels = dict(self.STATUS_CHOICES)
        return status_labels.get(self.effective_status, self.effective_status)

    def clean(self):
        if not self.member_id:
            return

        member = self.member

        if member.status != "active":
            raise ValidationError(
                "Only an active member can be assigned to a committee."
            )

    def save(self, *args, **kwargs):
        """
        একজন সদস্য একই ধরনের কমিটিতে একাধিক Active position
        রাখতে পারবে না।

        নতুন designation দিলে আগের active position
        automatically inactive হবে।
        """

        if self.is_active and self.member_id:

            existing_positions = CommitteeMember.objects.filter(
                member_id=self.member_id,
                committee_type=self.committee_type,
                is_active=True,
            ).exclude(
                pk=self.pk
            )

            existing_positions.update(
                is_active=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.member.member_id} - "
            f"{self.member.application.full_name} - "
            f"{self.get_designation_display()}"
        )


class Division(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Division"
        verbose_name_plural = "Divisions"

    def __str__(self):
        return self.name


class District(models.Model):
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name="districts",
    )
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["division", "name"],
                name="unique_district_per_division",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.division.name}"


class Upazila(models.Model):
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="upazilas",
    )
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["district", "name"],
                name="unique_upazila_per_district",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.district.name}"


class Municipality(models.Model):
    upazila = models.ForeignKey(
        Upazila,
        on_delete=models.CASCADE,
        related_name="municipalities",
    )
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["upazila", "name"],
                name="unique_municipality_per_upazila",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.upazila.name}"


class UnionWard(models.Model):
    upazila = models.ForeignKey(
        Upazila,
        on_delete=models.CASCADE,
        related_name="union_wards",
    )
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["upazila", "name"],
                name="unique_union_ward_per_upazila",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.upazila.name}"


class CommitteeMinimum(models.Model):
    committee_type = models.CharField(
        max_length=30,
        choices=CommitteeType.choices,
        unique=True,
    )

    minimum_members = models.PositiveIntegerField(
        default=0,
        help_text="Minimum number of members required for this committee.",
    )

    class Meta:
        ordering = ["committee_type"]
        verbose_name = "Committee Minimum"
        verbose_name_plural = "Committee Minimums"

    @property
    def committee_minimum(self):
        requirement = CommitteeMinimum.objects.filter(
            committee_type=self.committee_type
        ).first()

        return requirement.minimum_members if requirement else 0

    def __str__(self):
        return (
            f"{self.get_committee_type_display()} - "
            f"{self.minimum_members} members"
        )