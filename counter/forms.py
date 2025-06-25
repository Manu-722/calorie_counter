from django.shortcuts import render, redirect
from .models import FoodItem
from .forms import FoodItemForm

def index(request):
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

    return render(request, 'counter/index.html', {
        'form': form,
        'foods': foods,
        'total_calories': total_calories,
    })

def delete_item(request, id):
    FoodItem.objects.get(id=id).delete()
    return redirect('index')