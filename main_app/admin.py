from django.contrib import admin

# Register your models here.
from .models import Skill, Post

admin.site.register(Skill)
admin.site.register(Post)