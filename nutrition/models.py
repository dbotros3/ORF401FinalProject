from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()



class FoodItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fdc_id = models.CharField(max_length=100, verbose_name="FDC ID")
    name = models.CharField(max_length=200)
    calories = models.FloatField(help_text="Calories per 100g serving")
    protein = models.FloatField(help_text="Protein in grams per 100g serving")
    carbs = models.FloatField(help_text="Carbohydrates in grams per 100g serving")
    fats = models.FloatField(help_text="Fats in grams per 100g serving")

class FoodEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    servings = models.FloatField(default=1, help_text="Number of servings consumed")
    serving_size = models.FloatField(default=100, help_text="Serving size in grams per serving consumed")
    date = models.DateField()

class DailyNutrition(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    total_calories = models.FloatField(default=0)
    total_protein = models.FloatField(default=0)
    total_carbs = models.FloatField(default=0)
    total_fats = models.FloatField(default=0)

    def update_totals(self):
        entries = FoodEntry.objects.filter(user=self.user, date=self.date)
        self.total_calories = sum((entry.food_item.calories / 100) * entry.serving_size * entry.servings for entry in entries)
        self.total_protein = sum((entry.food_item.protein / 100) * entry.serving_size * entry.servings for entry in entries)
        self.total_carbs = sum((entry.food_item.carbs / 100) * entry.serving_size * entry.servings for entry in entries)
        self.total_fats = sum((entry.food_item.fats / 100) * entry.serving_size * entry.servings for entry in entries)
        self.save()
