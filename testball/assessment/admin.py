from django.contrib import admin
from testball.assessment.models import (
    QuizAttempt,
    QuestionAttempt,
    Progress,
    CommunitySolution,
)

admin.site.register(QuizAttempt)
admin.site.register(QuestionAttempt)
admin.site.register(Progress)
admin.site.register(CommunitySolution)
