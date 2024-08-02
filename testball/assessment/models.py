from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from testball.core.model_mixins import (
    UUIDMixin,
)
from testball.quiz.models import (
    Choice,
    Question,
    Quiz, 
)

Users = get_user_model()

# QuizAttempt model
class QuizAttempt(UUIDMixin):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField()
    time_taken = models.DurationField()
    completed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} - {self.quiz}'

# QuestionAttempt model
class QuestionAttempt(UUIDMixin):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='question_attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    answer_text = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return f'{self.quiz_attempt} - {self.question}'
    
# Progress Tracking
class Progress(UUIDMixin):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='progress')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score_improvement = models.FloatField()
    time_spent = models.DurationField()
    strengths = models.TextField()
    weaknesses = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.quiz}'
    

# Solution model for community solutions
class CommunitySolution(UUIDMixin):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='solutions')
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    solution_text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} - {self.question}'