from django import forms
from .models import PersonalInformation

class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'gender']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd-mm-yyyy'}),
        }