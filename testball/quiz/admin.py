from django.contrib import admin
from .models import (
    ExamCategory, 
    TestCategory, 
    Quiz, 
    Tag, 
    Question, 
    Choice, 
)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1  # Number of extra forms to display
    fields = ['choice_text', 'is_correct', 'multimedia_content']


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ['question_text', 'question_type', 'multimedia_content']
    inlines = [ChoiceInline]


class TagInline(admin.TabularInline):
    model = Quiz.tags.through  # Many-to-many relationship
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'is_public']
    search_fields = ['title', 'description']
    list_filter = ['created_by', 'is_public', 'test_category']
    inlines = [QuestionInline, TagInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('tags', 'questions')


admin.site.register(ExamCategory)
admin.site.register(TestCategory)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Tag)
# admin.site.register(Blog)

