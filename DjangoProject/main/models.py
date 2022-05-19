from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Images(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, max_length=50)
    imageFile = models.FileField(upload_to= 'documents/%Y/%m/%d/images/', max_length = 50)
    stegoFile = models.FileField(upload_to= 'documents/%Y/%m/%d/stego/', max_length = 50)