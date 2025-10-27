from django.contrib import admin
from .models import Profile, Lesson, Slide, Quiz, LessonProgress


class SlideInline(admin.TabularInline):
    model = Slide
    extra = 1
    fields = ("order", "title", "text", "image", "code")
    ordering = ["order"]


class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 2
    fields = ("question", "option_a", "option_b", "option_c", "option_d", "correct_option")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created_at")
    search_fields = ("title",)
    inlines = [SlideInline, QuizInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "xp")  # assumes Profile has an 'xp' field
    search_fields = ("user__username",)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed", "completed_slides", "updated_at")
    list_filter = ("completed", "lesson")
    search_fields = ("user__username", "lesson__title")
