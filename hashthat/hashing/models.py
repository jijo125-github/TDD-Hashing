from django.db import models

class Hash(models.Model):
    text = models.TextField()
    haash = models.CharField(max_length=64)

