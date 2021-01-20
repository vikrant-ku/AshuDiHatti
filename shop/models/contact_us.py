from django.db import models
from datetime import datetime


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    message = models.TextField()
    datetime = models.DateTimeField(default=datetime.now, blank=True)


    def __str__(self):
        return self.name
