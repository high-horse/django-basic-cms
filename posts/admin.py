from django.contrib import admin
# from .models import Post
# from .models import
from .models import models

# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Comment)