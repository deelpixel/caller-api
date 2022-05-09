from asyncio.windows_events import NULL
from django.db import models
from pandas import unique
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class RegisterUsers(models.Model):
    name = models.CharField(max_length=60)
    phone = PhoneNumberField(null=False, blank=False, unique=True)  
    password = models.CharField(max_length=50)
    email =models.EmailField(max_length=254, blank=True)
    def __str__(self):
        return f"{self.phone}"

class Spam(models.Model):
    phone = PhoneNumberField(null=False, blank=False,unique=True)
    spam=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.phone}"
class Global(models.Model):
    name = models.CharField(max_length=60)
    phone = PhoneNumberField(null=False, blank=False)
    registeruser=models.ForeignKey(RegisterUsers,on_delete=models.CASCADE,default=NULL)
    registered=models.BooleanField(default=False)
    spam=models.IntegerField(default=0)
    def __str__(self):
        return f'{self.name}\t{self.phone}'


