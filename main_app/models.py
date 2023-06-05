from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator 
from datetime import date

# Create your models here.
class Skill(models.Model):
    skill = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    categories = ArrayField(models.CharField(max_length=50))
    startDate = models.DateField('start of skill experience')
    endDate = models.DateField('end of skill experience')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.skill} ({self.user.username})'
    
    def get_yrs_exp(self):
        delta = (self.endDate - self.startDate).days
        years = int(delta/365)
        months = int((delta%365)/12)
        return f'{years} yrs {months} months'
    
class Post(models.Model):
    created = models.DateField('date created')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200) # need to come back when we know how much fits on a post card
    header = models.CharField(max_length=50) # change to headers
    contentBlock = models.TextField(max_length=200) # change to contentBlocks
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    savedBy = models.ManyToManyField(User)

    def __str__(self):
        return f'Title: {self.title} ({self.user.username})'

class File(models.Model):
    file = models.FileField
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # def is_photo(self):
    #     file_name, file_extension = os.path.splitext(self.url)
    #     return file_extension in ('.jpeg', '.JPG', '.JPEG', '.png', '.PNG', '.gif', '.ai', '.pdf', '.tiff', '.psd')

    # def is_vid(self):
    #     file_name, file_extension = os.path.splitext(self.url)
    #     return file_extension in ('.mp4', '.mov', '.avi')

