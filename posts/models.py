from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    """
    Messages that users can post.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    body = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.user, self.title)

    class Meta:
        ordering = ['-datetime']
