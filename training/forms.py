from django import forms
from .models import Certificate,User,Course


class CertificateUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.size > 15 * 1024 * 1024:  # 15 MB
            raise forms.ValidationError("File size must not exceed 15MB.")
        return file



class CourseAdminForm(forms.ModelForm):
    assign_all = forms.BooleanField(required=False,
        label="Assign to ALL employees",
        help_text="Check this to assign this course to all employees automatically."
    )
    employees = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign to selected employees",
        help_text="Select specific employees (ignored if 'Assign to ALL' is checked)."
    )

    class Meta:
        model = Course
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "employees" in self.fields:
            self.fields["employees"].queryset = User.objects.filter(groups__name="Employee")