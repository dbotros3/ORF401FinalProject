from django.conf import settings
from django.db import models

class Exercise(models.Model):
    STRENGTH_TRAINING = 'ST'
    CARDIO = 'CA'
    TYPE_CHOICES = [
        (STRENGTH_TRAINING, 'Strength Training'),
        (CARDIO, 'Cardio'),
    ]

    name = models.CharField(max_length=100)
    exercise_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=STRENGTH_TRAINING)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exercises_added',
                             null=True, blank=True)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_exercise_type_display()})"


class CardioWorkoutInstance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField()
    distance = models.FloatField(blank=True, null=True, help_text='Distance in miles')
    duration = models.IntegerField(blank=True, null=True, help_text='Duration of the workout in minutes')
    average_heart_rate = models.IntegerField(blank=True, null=True, help_text='Average heart rate (bpm)')

    def __str__(self):
        return f"{self.exercise.name} on {self.date}"


class StrengthWorkoutInstance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField()
    sets = models.IntegerField(blank=True, null=True, help_text='')
    reps = models.IntegerField(blank=True, null=True, help_text='')
    weight = models.FloatField(blank=True, null=True, help_text='(lbs)')

    def __str__(self):
        return f"{self.exercise.name} on {self.date}"


