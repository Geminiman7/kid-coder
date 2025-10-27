from django.shortcuts import render, redirect, get_object_or_404
# ✅ Import login/logout with aliases to avoid naming conflicts
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Lesson, Quiz, LessonProgress,Slide
import json

# -----------------------
# Home Page
# -----------------------
def home(request):
    return render(request, 'home.html')


# -----------------------
# Register View
# -----------------------
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validation checks
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        # Create user safely
        user = User.objects.create_user(username=username, email=email, password=password1)

        # Use get_or_create to avoid duplicate Profile errors
        Profile.objects.get_or_create(user=user)

        messages.success(request, "Account created successfully! Please log in.")
        # This redirect was failing because the 'login' view was broken
        return redirect('login')

    return render(request, 'register.html')


# -----------------------
# Login View (Corrected)
# -----------------------
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ✅ Use the aliased 'auth_login' function
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# -----------------------
# Logout View (Corrected)
# -----------------------
def logout(request):
    # ✅ Use the aliased 'auth_logout' function
    auth_logout(request)
    return redirect('home')


# -----------------------
# Dashboard
# -----------------------
@login_required
def dashboard(request):
    profile = request.user.profile
    lessons = Lesson.objects.all().order_by('-created_at')
    progress = LessonProgress.objects.filter(user=request.user)
    completed_ids = [p.lesson.id for p in progress if p.completed]

    return render(request, 'dashboard.html', {
        'profile': profile,
        'lessons': lessons,
        'completed_ids': completed_ids
    })


# -----------------------
# Lesson Detail
# -----------------------
@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    slides = lesson.slides.all().order_by("order")  # assuming related_name='slides'
    return render(request, "lesson_detail.html", {"lesson": lesson, "slides": slides})

# -----------------------
# Take Quiz (Corrected)
# -----------------------
@login_required
def quiz(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quizzes = Quiz.objects.filter(lesson=lesson)

    if request.method == 'POST':
        score = 0
        for quiz in quizzes:
            selected = request.POST.get(str(quiz.id))
            if selected == quiz.correct_option:
                score += 1
        
        total = quizzes.count()
        
        # ✅ Fix: Check if total is zero to avoid ZeroDivisionError
        percent = 0
        if total > 0:
            percent = int((score / total) * 100)

        if percent >= 70:
            LessonProgress.objects.update_or_create(
                user=request.user, lesson=lesson, defaults={'completed': True}
            )
            request.user.profile.xp += 10
            request.user.profile.save()
            messages.success(request, f"🎉 You passed! Score: {percent}% XP +10")
        else:
            messages.warning(request, f"😕 You scored {percent}%. Try again!")

        return redirect('dashboard')

    return render(request, 'quiz.html', {'lesson': lesson, 'quizzes': quizzes})