from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Document(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(blank=False, null=False)
    total_vote = models.IntegerField(default=0, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.name, self.category.title)


class ControlVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.category, self.status)


class Comment(models.Model):
    document = models.ForeignKey(
        Document, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)
