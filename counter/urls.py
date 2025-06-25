from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:id>/', views.delete_item, name='delete_item'),
    path('history/', views.history, name='history'),
]