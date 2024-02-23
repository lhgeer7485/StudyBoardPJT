from django.db import models
from django.conf import settings

# Create your models here.
class Problem(models.Model):
    solved_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='solved_problems')
    name = models.CharField(max_length=30)
    problem_num = models.IntegerField()
    rank = models.CharField(max_length=5)


class ProblemClass(models.Model):
    problems = models.ManyToManyField(Problem, related_name='classes')
    name = models.CharField(max_length=30)
    ProblemClass_num = models.IntegerField(blank=True)

class Algorithm(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_algotithms'
    )
    problem = models.ForeignKey(Problem, related_name='algorithms',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

