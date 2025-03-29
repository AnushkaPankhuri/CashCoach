from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.date} | {self.category} | ₹{self.amount}"

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    budget_threshold = models.FloatField(default=10000)
    
    def __str__(self):
        return f"{self.user.username}'s Settings (Budget: ₹{self.budget_threshold})"