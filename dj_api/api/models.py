from django.db import models

class GlassdoorQuestion(models.Model):
    date_posted = models.DateField()
    experience = models.TextField()
    question = models.TextField()
