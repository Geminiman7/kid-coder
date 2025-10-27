from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('quiz/<int:lesson_id>/', views.quiz, name='quiz'),
]
