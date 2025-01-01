from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, GiftCard, Rating

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class GiftCardForm(forms.ModelForm):
    class Meta:
        model = GiftCard
        fields = ['retailer', 'value', 'code', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'})
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']