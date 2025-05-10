from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),  # Путь к личному кабинету
    path('profile/delete/', views.delete_profile, name='delete_profile'),  # Путь для удаления профиля
]
