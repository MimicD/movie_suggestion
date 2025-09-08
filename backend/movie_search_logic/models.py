from django.db import models
from pgvector.django import VectorField

class Movie(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    original_language = models.CharField(max_length=25, null=True, blank=True)

    embedding = VectorField(dimensions=384, null=True, blank=True)

    class Meta:
        unique_together = ('title', 'release_date')

    def set_embedding(self, embedding_vector):
        self.embedding = embedding_vector
        self.save()