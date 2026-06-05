from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('abonelikler/', views.subscription_list, name='subscription_list'),
    # Subscription CRUD
    path('add/', views.subscription_add, name='subscription_add'),
    path('edit/<int:pk>/', views.subscription_edit, name='subscription_edit'),
    path('delete/<int:pk>/', views.subscription_delete, name='subscription_delete'),
    path('cancel/<int:pk>/', views.subscription_cancel, name='subscription_cancel'),
    # Credit Card CRUD
    path('cards/', views.card_list, name='card_list'),
    path('cards/add/', views.card_add, name='card_add'),
    path('cards/edit/<int:pk>/', views.card_edit, name='card_edit'),
    path('cards/delete/<int:pk>/', views.card_delete, name='card_delete'),
]
