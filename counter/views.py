from django.shortcuts import render, redirect
from .models import FoodItem
from .forms import FoodItemForm
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from datetime import date

def index(request):
    """Display form, list of food items, total calories, and handle add/reset POST actions."""
    form = FoodItemForm()
    foods = FoodItem.objects.all()
    total_calories = sum(item.calories for item in foods)

    if request.method == 'POST':
        if 'add' in request.POST:
            form = FoodItemForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        elif 'reset' in request.POST:
            FoodItem.objects.all().delete()
            return redirect('index')

    return render(request, 'index.html', {
        'form': form,
        'foods': foods,
        'total_calories': total_calories,
    })

def delete_item(request, id):
    """Delete a specific food item by ID."""
    FoodItem.objects.filter(id=id).delete()
    return redirect('index')

@login_required
def history(request):
    """Group food items by date and calculate daily totals."""
    items = FoodItem.objects.order_by('-created_at')
    grouped = defaultdict(list)

    for item in items:
        grouped[item.created_at].append(item)

    entries = [
        {
            'date': date_key,
            'items': grouped[date_key],
            'total': sum(i.calories for i in grouped[date_key])
        }
        for date_key in sorted(grouped.keys(), reverse=True)
    ]

    return render(request, 'history.html', {'entries': entries})