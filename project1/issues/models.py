from django.db import models
from django.conf import settings


# Create your models here.
class Issue(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_issues'
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_issues'
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
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments_issue')
    comment_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='issue_comments'
    )
    like_comment_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_comments_issue'
    )
    comment_content = models.CharField(max_length=200)
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_updated_at = models.DateTimeField(auto_now=True)
