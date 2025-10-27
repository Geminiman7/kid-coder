from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

LEVEL_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    badges = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User

# ==============================
# LESSON & SLIDE STRUCTURE
# ==============================

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Slide(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="slides")
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="slides/", blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


# ==============================
# QUIZ SYSTEM (Compatible)
# ==============================

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="quizzes")
    question = models.CharField(max_length=300)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])

    def __str__(self):
        return f"Quiz for {self.lesson.title}"


# ==============================
# USER PROGRESS TRACKING (Optional)
# ==============================

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_slides = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({'Done' if self.completed else 'In Progress'})"
