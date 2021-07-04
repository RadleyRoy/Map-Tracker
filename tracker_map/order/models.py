from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

USER_CHOICES = [
    (1, 'Admins'),
    (2, 'Buyers'),
    (3, 'Vendors'),
    (4, 'Runners')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.IntegerField(choices=USER_CHOICES, default=2)

    def __str__(self):
        return self.user.username



class Address(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200)
    pin = models.IntegerField(validators=[MaxValueValidator(999999), MinValueValidator(100000)])
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    is_primary = models.BooleanField(default=True)

    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Runner(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    max_orders = models.IntegerField(default=10)
    current_orders = models.IntegerField(default=0)

class Product(models.Model):
    name = models.CharField(max_length=200)
    detail = models.CharField(max_length=1000)
    vendor = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Order(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    ordered_at = models.DateTimeField(auto_now_add=True)
    expected_at = models.DateTimeField(null=True, blank=True)

STATUS_CHOICES = [
    (1, 'Order received'),
    (2, 'Out for delivery'),
    (3, 'Delivery Received')
]

class Status(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Statuses'
