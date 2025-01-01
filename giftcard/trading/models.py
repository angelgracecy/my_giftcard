from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class User(AbstractUser):
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_ratings = models.PositiveIntegerField(default=0)

class GiftCard(models.Model):
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('failed', 'Failed'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='giftcards')
    retailer = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=100, unique=True)
    expiration_date = models.DateField()
    is_available = models.BooleanField(default=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.retailer} - ${self.value}"

class Trade(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)