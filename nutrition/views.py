from django.http import JsonResponse, HttpResponse
from .utils import search_usda_food
import requests
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import FoodItem, FoodEntry, DailyNutrition
from django.utils.dateparse import parse_date
import datetime
from .forms import FoodItemForm
import openai
from django.contrib.auth.decorators import login_required

def food_details(request):
    fdc_id = request.GET.get('fdcId')
    api_key = 'zYxRawipSZYiv1a8XHQgVwHDk3RNvZHj5jD02XVi'
    details_url = f'https://api.nal.usda.gov/fdc/v1/food/{fdc_id}'
    params = {'api_key': api_key}
    response = requests.get(details_url, params=params)
    food_details = response.json()

    nutrients = {
        "calories": get_nutrient(food_details, '2047'),
        "protein": get_nutrient(food_details, '1003'),
        "carbs": get_nutrient(food_details, '1005'),
        "fats": get_nutrient(food_details, '1004')
    }
    return JsonResponse(nutrients)

def get_nutrient(food_details, nutrient_id):
    for nutrient in food_details.get('foodNutrients', []):
        if nutrient['nutrientId'] == nutrient_id:
            return nutrient['value']
    return 0

def autocomplete(request):
    query = request.GET.get('term', '')
    api_key = 'zYxRawipSZYiv1a8XHQgVwHDk3RNvZHj5jD02XVi'
    results = search_usda_food(query, api_key)
    suggestions = [{'label': food['description'], 'value': food['fdcId']} for food in results] if results else []
    return JsonResponse(suggestions, safe=False)


@login_required
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            try:
                food_item = form.save(commit=False)
                food_item.user = request.user
                food_item.save()
                print(f'FoodItem created: {food_item}')

                servings = request.POST.get('servings', 1)
                serving_size = request.POST.get('serving-size', 100)
                date_str = request.POST.get('date', timezone.now().date().isoformat())

                try:
                    entry_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    entry_date = timezone.now().date()

                food_entry = FoodEntry(
                    user=request.user,
                    food_item=food_item,
                    servings=servings,
                    serving_size=serving_size,
                    date=entry_date
                )
                food_entry.save()
                print(f'Created FoodEntry: {food_entry}')

                daily_nutrition, created = DailyNutrition.objects.get_or_create(user=request.user, date=entry_date)
                daily_nutrition.update_totals()
                print(f'Updated DailyNutrition: {daily_nutrition}')

                return redirect('nutrition:daily_nutrition')
            except Exception as e:
                print(f"Error while creating food item or entry: {e}")
                return render(request, 'nutrition/add_food.html', {'form': form})
        else:
            print("Form is not valid")
            print(form.errors)
            return render(request, 'nutrition/add_food.html', {'form': form})
    else:
        form = FoodItemForm()
        return render(request, 'nutrition/add_food.html', {'form': form})

@login_required
def daily_nutrition_view(request):
    date_str = request.GET.get('date')
    if date_str:
        date = parse_date(date_str)
        if not date:
            date = timezone.now().date()
    else:
        date = timezone.now().date()

    daily_nutrition, created = DailyNutrition.objects.get_or_create(user=request.user, date=date)
    food_entries = FoodEntry.objects.filter(user=request.user, date=date)

    daily_nutrition.update_totals()

    context = {
        'food_entries': food_entries,
        'daily_nutrition': daily_nutrition,
        'date': date
    }
    return render(request, 'nutrition/daily_nutrition.html', context)

@login_required
def ask_food_question(request):
    context = {}
    if request.method == 'POST':
        question = request.POST.get('question')
        try:
            openai.api_key = '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'
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. List three food suggestions that meet the specified nutritional goals, formatted as bullet points."},
                    {"role": "user", "content": question}
                ],
                max_tokens=150
            )
            if response['choices']:
                answer = response['choices'][0]['message']['content']
                processed_answer = [line.strip()[2:] if line.startswith('- ') else line.strip() for line in answer.split('\n') if line.strip()]
                context['answer'] = processed_answer
            else:
                context['error'] = "No response from the AI."
        except Exception as e:
            context['error'] = str(e)
    return render(request, 'nutrition/ask_question.html', context)
