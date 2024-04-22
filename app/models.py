from django.db import models
from .models import *

class Student(models.Model):
    age = models.IntegerField(verbose_name="Age")
    fullname = models.CharField(verbose_name="fullname", max_length=100, null=True,blank=True)
    Registered_date = models.DateField(verbose_name="Registered date", auto_now_add=True)
    Updated_date = models.DateField(verbose_name="Updated date", auto_now=True)
    class Meta:
        verbose_name = "Student"
    def __str__(self):
        return self.fullname
    #calculate Z score for adminsite
    def calculate_z_score(self):
        mean_age = Student.objects.all().aggregate(models.Avg('age'))['age__avg']
        std_dev_age = Student.objects.all().aggregate(models.StdDev('age'))['age__stddev']
        z_score = (self.age - mean_age) / std_dev_age
        return z_score

