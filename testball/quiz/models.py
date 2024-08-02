from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from testball.core.model_mixins import (
    SlugMixin,
    UUIDMixin,
)

User = get_user_model()

# Exam Category model
class ExamCategory(SlugMixin, UUIDMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TestCategory(SlugMixin, UUIDMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    exam_category = models.ForeignKey(ExamCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

# Quiz model
class Quiz(UUIDMixin):
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='created_by_quizzes')
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    test_category = models.ForeignKey(TestCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    time_limit = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.title

# Tag model
class Tag(SlugMixin, UUIDMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Question model
class Question(UUIDMixin):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice Question'),
        ('TF', 'True/False'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=5, choices=QUESTION_TYPES)
    multimedia_content = models.FileField(upload_to='questions/multimedia/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question_text

# Choice model for MCQ
class Choice(UUIDMixin):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    multimedia_content = models.FileField(upload_to='questions/multimedia/', blank=True, null=True)

    def __str__(self):
        return self.choice_text

# Blog model
class Blog(SlugMixin, UUIDMixin):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


#TODO:
'''
# Resource Link model
class ResourceLink(models.Model):
    pass

# Notifications and Reminders
class Notification(models.Model):
    pass
'''