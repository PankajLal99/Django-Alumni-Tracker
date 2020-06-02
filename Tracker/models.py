from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import datetime

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    RollNo=models.CharField(max_length=20,null=True,unique=True)
    Year=models.IntegerField(null=True)
    Branch=models.CharField(max_length=20,null=True)
    Image=models.ImageField(upload_to='AlumniTracker/images',default="static/images/profile.png")
    phone_regex = RegexValidator(regex=r'^\+?\d[\d -]{8,12}\d')
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True,null=True)
    Current_Location=models.CharField(max_length=30,null=True)
    Work_profile=models.CharField(max_length=30,null=True,blank=True)
    Connection=models.CharField(max_length=10,null=True,blank=True)
    Company=models.CharField(max_length=50,null=True,blank=True)
    Joining=models.CharField(max_length=20,null=True,blank=True)
    College=models.CharField(max_length=50,null=True)
    Degree=models.CharField(max_length=20,null=True)
    linkedIn_Link=models.CharField(max_length=100)

# Adding Scrapping Database
class Scrapper_Data(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True, null=True)
    profile_title = models.CharField(max_length=100,blank=True, null=True)
    location = models.CharField(max_length=100,blank=True, null=True)
    connection = models.CharField(max_length=15,blank=True, null=True)
    experience = models.CharField(max_length=50,blank=True, null=True)
    job_title = models.CharField(max_length=50,blank=True, null=True)
    joining_date = models.CharField(max_length=50,blank=True, null=True)
    college_name = models.CharField(max_length=100,blank=True, null=True)
    degree_name = models.CharField(max_length=50,blank=True, null=True)
    stream = models.CharField(max_length=50,blank=True, null=True)
    degree_year = models.CharField(max_length=100,blank=True, null=True)


STATUS = (
    (0,"Requested"),
    (1,"Publish")
)
class Blog(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=50,default='Admin')
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='AlumniTracker/images',default="static/images/bg.jpg")
    status = models.IntegerField(choices=STATUS, default=0)



    
