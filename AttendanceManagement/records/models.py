# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.urls import reverse

# Create your models here.
# class Records(models.Model):
#     id = models.CharField(max_length=100, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50, null=True)
#     residence = models.CharField(max_length=50, null=True)
#     country = models.CharField(max_length=50, null=True)
#     education = models.CharField(max_length=150, null=True)
#     occupation = models.CharField(max_length=150, null=True)
#     marital_status = models.CharField(max_length=50, null=True)
#     bio = models.TextField()
#     recorded_at = models.DateTimeField(default=datetime.now, blank=True)

#     def __str__(self):
#         return self.first_name
#     class Meta:
#         verbose_name_plural = "Records"
class student(models.Model):
    usn = models.CharField(max_length=12,primary_key=True)
    first_name = models.CharField(max_length=50)
    email=models.EmailField(max_length=75,null=True)
    last_name = models.CharField(max_length=50, null=True)
    def get_absolute_url(self):
       return reverse('test:student-details',kwargs={'id':self.usn})
    
    def __str__(self):
        return self.usn
    
    

class teacher(models.Model):
    pid = models.CharField(max_length=12,primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    attendance= models.IntegerField(default=0)
    subcode =models.CharField(max_length=12,null=True)
    def get_absolute_url(self):
       return reverse('test:details-teacher',kwargs={'id':self.pid})
    def __str__(self):
        return self.pid +'-'+ self.first_name

class subjects(models.Model):
    subcode =models.CharField(max_length=12,primary_key=True)
    usn=models.ManyToManyField(student,null=True)
    pid=models.ForeignKey(teacher,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.subcode
class attendances(models.Model):
    subcode =models.ForeignKey(subjects,on_delete=models.CASCADE,null=True)
    attendance= models.IntegerField(default=0)
    usn =models.ForeignKey(student,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.usn )+'-'+ str(self.subcode)


