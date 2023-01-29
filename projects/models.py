from django.db import models

# Create your models here.
class Payment(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    surname = models.CharField(max_length=50, null=False, blank=False)
    card_number = models.CharField(max_length=50, null=False, blank=False, unique=True)
    card_cvv = models.IntegerField(null=False, blank=False)
    total_value = models.IntegerField(null=False, blank=False)
    extra_description = models.CharField(max_length=500, null=True, blank=True)
    comission_value = models.FloatField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)