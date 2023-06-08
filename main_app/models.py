from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator 
from datetime import date
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import os


# Create your models here.
class Skill(models.Model):
    skill = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    categories = ArrayField(models.CharField(max_length=50))
    startDate = models.DateField()
    endDate = models.DateField(null=True, blank=True)
    isOngoing = models.BooleanField(default=False)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.skill} ({self.user.username})'
    
    def get_yrs_exp(self):
        delta = (self.endDate - self.startDate).days
        years = int(delta/365)
        months = int((delta%365)/12)
        return f'{years} yrs {months} months'
    
    def get_absolute_url(self):
        return reverse('home_feed_list')
    
    # FIGURE OUT LATER
    # def post(self, request, *args, **kwargs):
    #     print('hi1')
    #     if request.isOngoing:
    #         print('hi')
    #         self.endDate = timezone.now;
    #     return super().post(request, *args, **kwargs)
    
class Post(models.Model):
    created = models.DateField('date created', default=timezone.now)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200) # need to come back when we know how much fits on a post card
    header = models.CharField(max_length=50) # change to headers
    contentBlock = models.TextField(max_length=10000) # change to contentBlocks
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    savedBy = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'Title: {self.title} ({self.creator.username})'
    
    def get_absolute_url(self):
        return reverse('home_feed_list')
    
    def get_points(self, keywords):
        title_list = self.title.split()
        description_list = self.description.split()
        header_list = self.header.split()
        content_list = self.contentBlock.split()
        word_list = title_list + description_list + header_list + content_list

        points = 0
        for keyword in keywords:
            for word in word_list:
                if keyword.lower() == word.lower(): points += 1
        return points
    
class Review(models.Model):
    created = models.DateField('date created', default=timezone.now)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField(max_length=500, null=True, blank=True) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rating} star review for {self.post}'

    def get_absolute_url(self):
        return reverse('posts_detail', kwargs={'pk': self.post.id})

class File(models.Model):
    url = models.CharField(default='.jpg')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def is_photo(self):
        file_name, file_extension = os.path.splitext(self.url)
        return file_extension in ('.jpeg', '.JPG', '.JPEG', '.png', '.PNG', '.gif', '.ai', '.pdf', '.tiff', '.psd')

    def is_vid(self):
        file_name, file_extension = os.path.splitext(self.url)
        return file_extension in ('.mp4', '.mov', '.avi', '.MOV')

    def __str__(self):
        return f"File for {self.post} - {self.url}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='curr_user')
    bio = models.TextField(max_length=400, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    followers = models.ManyToManyField(User, related_name='follower')
    following = models.ManyToManyField(User)

    def __str__(self):
        return f'Profile for {self.user}'

    def get_absolute_url(self):
        return reverse('home_feed_list')
