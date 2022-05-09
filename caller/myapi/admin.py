from django.contrib import admin
from .models import RegisterUsers,Spam,Global
# Register your models here.

admin.site.register(RegisterUsers)
admin.site.register(Spam)
admin.site.register(Global)