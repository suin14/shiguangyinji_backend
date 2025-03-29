from django.db import models
from django.contrib.auth.models import User

from shiguangyinji import settings


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='owner_id')
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'document')


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'document')


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    doc = models.ForeignKey(Document, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by User {self.user_id} on {self.doc.title}"

