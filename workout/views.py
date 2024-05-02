from django.shortcuts import render, redirect
from .forms import ExerciseForm
from django.db.models import Q
from .forms import CardioWorkoutInstanceForm, StrengthWorkoutInstanceForm
from django.shortcuts import render, get_object_or_404
from .models import Exercise, CardioWorkoutInstance, StrengthWorkoutInstance
from django.contrib.auth.decorators import login_required






def home(request):
    return render(request, 'home.html')

@login_required
def add_exercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()

        custom_name = request.POST.get('custom_name')
        if custom_name:
            Exercise.objects.create(
                name=custom_name,
                exercise_type=request.POST.get('custom_type'),
                user=request.user,
                is_custom=True,
            )
        return redirect('workout:view_exercises')
    else:
        form = ExerciseForm()
        predefined_exercises = Exercise.objects.filter(is_custom=False)

    return render(request, 'workout/add_exercise.html', {
        'form': form,
        'predefined_exercises': predefined_exercises
    })

@login_required
def view_exercises(request):
    exercises = Exercise.objects.filter(Q(user=request.user) | Q(is_custom=False))
    return render(request, 'workout/view_exercises.html', {'exercises': exercises})

@login_required
def add_cardio_workout_instance(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id, exercise_type='CA')

    if request.method == 'POST':
        form = CardioWorkoutInstanceForm(request.POST)
        if form.is_valid():
            workout_instance = form.save(commit=False)
            workout_instance.exercise = exercise
            workout_instance.user = request.user
            workout_instance.save()
            return redirect('workout:view_exercises')
    else:
        form = CardioWorkoutInstanceForm(initial={'exercise': exercise})

    return render(request, 'workout/add_cardio_workout_instance.html', {'form': form, 'exercise': exercise})

@login_required
def add_strength_workout_instance(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id, exercise_type='ST')

    if request.method == 'POST':
        form = StrengthWorkoutInstanceForm(request.POST)
        if form.is_valid():
            workout_instance = form.save(commit=False)
            workout_instance.exercise = exercise
            workout_instance.user = request.user
            workout_instance.save()
            return redirect('workout:view_exercises')
    else:
        form = StrengthWorkoutInstanceForm(initial={'exercise': exercise})

    return render(request, 'workout/add_strength_workout_instance.html', {'form': form, 'exercise': exercise})


@login_required
def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if exercise.exercise_type == 'CA':
        instances = CardioWorkoutInstance.objects.filter(exercise=exercise, user=request.user).order_by('date')
        dates = [instance.date.strftime('%Y-%m-%d') for instance in instances]
        data = {
            'durations': [instance.duration for instance in instances],
            'distances': [instance.distance for instance in instances],
            'average_heart_rate': [instance.average_heart_rate for instance in instances],

        }
    elif exercise.exercise_type == 'ST':
        instances = StrengthWorkoutInstance.objects.filter(exercise=exercise, user=request.user).order_by('date')
        dates = [instance.date.strftime('%Y-%m-%d') for instance in instances]
        data = {
            'weights': [instance.weight for instance in instances],
            'reps': [instance.reps for instance in instances],
            'sets': [instance.sets for instance in instances],
        }

    form_class = CardioWorkoutInstanceForm if exercise.exercise_type == 'CA' else StrengthWorkoutInstanceForm
    form = form_class(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        workout_instance = form.save(commit=False)
        workout_instance.exercise = exercise
        workout_instance.user = request.user
        workout_instance.save()
        return redirect('workout:exercise_detail', exercise_id=exercise_id)

    context = {
        'exercise': exercise,
        'instances': instances,
        'form': form,
        'dates': dates,
        **data
    }
    return render(request, 'workout/exercise_detail.html', context)







