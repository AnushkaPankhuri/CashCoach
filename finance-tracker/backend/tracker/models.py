from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     email = models.EmailField(unique=True)
    
#     def __str__(self):
#         return self.username

class Transaction(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user',) 

    def __str__(self):
        return f"{self.user.username}'s Budget: ₹{self.amount}"