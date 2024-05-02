from django import forms
from .models import Exercise
from .models import CardioWorkoutInstance, StrengthWorkoutInstance


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'exercise_type', 'description']


class CardioWorkoutInstanceForm(forms.ModelForm):
    class Meta:
        model = CardioWorkoutInstance
        fields = ['date', 'distance', 'duration', 'average_heart_rate']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'distance': forms.NumberInput(attrs={'step': '0.01'}),
            'duration': forms.NumberInput(attrs={'min': 0, 'placeholder': ''}),
            'average_heart_rate': forms.NumberInput(attrs={'min': 0, 'placeholder': ''}),
        }


class StrengthWorkoutInstanceForm(forms.ModelForm):
    class Meta:
        model = StrengthWorkoutInstance
        fields = ['date', 'sets', 'reps', 'weight']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'sets': forms.NumberInput(attrs={'min': 0}),
            'reps': forms.NumberInput(attrs={'min': 0}),
            'weight': forms.NumberInput(attrs={'min': 0, 'step': 0.5}),
        }


