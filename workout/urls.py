from django.urls import path
from . import views


app_name = 'workout'

urlpatterns = [
    path('add_exercise/', views.add_exercise, name='add_exercise'),
    path('view_exercises/', views.view_exercises, name='view_exercises'),
    path('add_cardio_instance/<int:exercise_id>/', views.add_cardio_workout_instance, name='add_cardio_instance'),
    path('add_strength_instance/<int:exercise_id>/', views.add_strength_workout_instance, name='add_strength_instance'),
    path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
]
