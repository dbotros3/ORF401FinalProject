from django import forms
from .models import FoodItem

class FoodItemForm(forms.ModelForm):
    name = forms.CharField(
        label='Food Name',
        widget=forms.TextInput(attrs={
            'id': 'food-name',
            'autocomplete': 'off',
            'placeholder': 'Start typing a food name...'
        }),
    )

    class Meta:
        model = FoodItem
        fields = ('name', 'calories', 'protein', 'carbs', 'fats')
        widgets = {
            'calories': forms.NumberInput(attrs={'readonly': True}),
            'protein': forms.NumberInput(attrs={'readonly': True}),
            'carbs': forms.NumberInput(attrs={'readonly': True}),
            'fats': forms.NumberInput(attrs={'readonly': True}),
        }
