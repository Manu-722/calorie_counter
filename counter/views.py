from django.shortcuts import render, redirect
from .models import FoodItem
from .forms import FoodItemForm
from django.contrib.auth.decorators import login_required


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
    return render(request, 'history.html')
