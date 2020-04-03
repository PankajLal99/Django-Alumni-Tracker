from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    RollNo=models.CharField(max_length=20,null=True,unique=True)
    Year=models.IntegerField(null=True)
    Branch=models.CharField(max_length=20,null=True)
    Image=models.ImageField(upload_to='AlumniTracker/images',default="AlumniTracker/images/profile.png")
    Current_Location=models.CharField(max_length=30,null=True)
    Work_profile=models.CharField(max_length=30,null=True,blank=True)
    Connection=models.CharField(max_length=10,null=True,blank=True)
    Company=models.CharField(max_length=50,null=True,blank=True)
    Joining=models.CharField(max_length=20,null=True,blank=True)
    College=models.CharField(max_length=50,null=True)
    Degree=models.CharField(max_length=20,null=True)
    linkedIn_Link=models.CharField(max_length=100,null=True,blank=True)

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
    college_name = models.CharField(max_length=50,blank=True, null=True)
    degree_name = models.CharField(max_length=50,blank=True, null=True)
    stream = models.CharField(max_length=50,blank=True, null=True)
    degree_year = models.CharField(max_length=100,blank=True, null=True)


    