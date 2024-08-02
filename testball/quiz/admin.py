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
    extra = 1
    fields = ['choice_text', 'is_correct', 'multimedia_content']


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ['question_text', 'question_type', 'multimedia_content']
    inlines = [ChoiceInline]


class TagInline(admin.TabularInline):
    model = Quiz.tags.through
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'is_public']
    search_fields = ['title', 'description']
    list_filter = ['created_by', 'is_public', 'test_category']
    inlines = [TagInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('tags', 'questions')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type', 'quiz', 'created_at']
    search_fields = ['question_text']
    list_filter = ['question_type', 'quiz']
    inlines = [ChoiceInline]


admin.site.register(ExamCategory)
admin.site.register(TestCategory)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Blog)

