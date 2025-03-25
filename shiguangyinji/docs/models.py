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

