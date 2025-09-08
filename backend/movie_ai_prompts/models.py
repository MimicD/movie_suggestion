from django.db import models
from pgvector.django import VectorField


class Prompt(models.Model):
    text = models.CharField(max_length=500)
    translated_text = models.CharField(max_length=500)
    author = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    date_created_at = models.DateTimeField(auto_now_add=True)
    response = models.JSONField(null=True, blank=True)

    embedding = VectorField(dimensions=384, null=True, blank=True)