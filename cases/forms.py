from django import forms # type: ignore
from .models import Case

class CaseForm(forms.ModelForm):
    date_of_crime = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Case
        fields = [
            'crime_type', 'location', 'date_of_crime',
            'victim_name', 'description', 'evidence_image', 'status'
        ]

    def clean_evidence_image(self):
        img = self.cleaned_data.get('evidence_image')
        if img:
            if img.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image too large (max 5MB).')
            valid = ['image/jpeg', 'image/png', 'image/jpg']
            if getattr(img, 'content_type', None) not in valid:
                raise forms.ValidationError('Invalid image type. Allowed: jpg, jpeg, png.')
        return img