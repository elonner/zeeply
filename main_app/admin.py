from django.contrib import admin

# Register your models here.
from .models import Skill, Post, Profile, Review

admin.site.register(Skill)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Review)