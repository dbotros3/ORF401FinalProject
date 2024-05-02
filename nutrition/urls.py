from django.urls import path
from .views import autocomplete
from .views import add_food
from .views import daily_nutrition_view
from .views import ask_food_question


app_name = 'nutrition'

urlpatterns = [
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('add-food/', add_food, name='add_food'),
    path('daily-nutrition/', daily_nutrition_view, name='daily_nutrition'),
    path('ask-food-question/', ask_food_question, name='ask-food-question'),
]
