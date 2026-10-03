from django import forms

from .models import (
    CommitteeMember,
    Division,
    District,
    Upazila,
    Municipality,
    UnionWard,
)


class CommitteeMemberAdminForm(forms.ModelForm):

    class Meta:
        model = CommitteeMember
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -----------------------------
        # Division
        # -----------------------------
        self.fields["division"].queryset = (
            Division.objects
            .all()
            .order_by("name")
        )

        # -----------------------------
        # District
        # -----------------------------
        self.fields["district"].queryset = District.objects.none()

        # -----------------------------
        # Upazila
        # -----------------------------
        self.fields["thana_upazila"].queryset = Upazila.objects.none()

        # -----------------------------
        # Municipality
        # -----------------------------
        self.fields["municipality"].queryset = (
            Municipality.objects.none()
        )

        # -----------------------------
        # Union / Ward
        # -----------------------------
        self.fields["union_ward"].queryset = (
            UnionWard.objects.none()
        )

        # ==========================================
        # Existing Committee Member Edit
        # ==========================================

        if self.instance and self.instance.pk:

            if self.instance.division_id:
                self.fields["district"].queryset = (
                    District.objects
                    .filter(
                        division_id=self.instance.division_id
                    )
                    .order_by("name")
                )

            if self.instance.district_id:
                self.fields["thana_upazila"].queryset = (
                    Upazila.objects
                    .filter(
                        district_id=self.instance.district_id
                    )
                    .order_by("name")
                )

            if self.instance.thana_upazila_id:

                self.fields["municipality"].queryset = (
                    Municipality.objects
                    .filter(
                        upazila_id=self.instance.thana_upazila_id
                    )
                    .order_by("name")
                )

                self.fields["union_ward"].queryset = (
                    UnionWard.objects
                    .filter(
                        upazila_id=self.instance.thana_upazila_id
                    )
                    .order_by("name")
                )