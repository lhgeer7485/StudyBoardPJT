from django.db import models
from django.conf import settings


# Create your models here.
class Plan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_plans'
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_plans'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    count = models.PositiveIntegerField(default=0)
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def update_count(self):
    #     self.count = self.count + 1
    #     self.save()


class Comment(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='comments')
    comment_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='plan_comments'
    )
    like_comment_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_comments'
    )
    comment_content = models.CharField(max_length=200)
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_updated_at = models.DateTimeField(auto_now=True)
