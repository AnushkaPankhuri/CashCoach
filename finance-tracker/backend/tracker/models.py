from django.db import models

# Create your models here.

from django.db import models

class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    amount = models.FloatField()

    def _str_(self):
        return f"{self.date} | {self.category} | ₹{self.amount}"