from django.db import models

class Series(models.Model):
    SOURCE_CHOICES = [
        ('TP2', 'TP2'),  # TurkPlayTV
        ('TP4', 'TP4'),  # TureckiiTV
    ]

    title = models.CharField(max_length=255)
    source = models.CharField(max_length=3, choices=SOURCE_CHOICES)
    url = models.URLField(unique=True)
    images = models.JSONField(default=list, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.source})"
