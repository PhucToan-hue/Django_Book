import datetime
from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    published_date = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return self.title