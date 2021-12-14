from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
from django.utils import timezone
import re
import bcrypt

Name_Regex = re.compile(r'^[A-Za-z ]+$')

# Create your models here.
class userManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "El nombre debe contener como min 2 caracteres"
        if len(postData['name']) > 15:
            errors["name"] = "El nombre debe contener como max 15 caracteres"
        if len(postData["password"]) < 8:
            errors["password"] = "la contraseña debe contener como min 8 caracteres"
        if postData["password"]!= postData["confirmp"]:
            errors["confirmpassword"]= 'Passwords don`t match'
        return errors
    def login_validator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email address!"
        email_check = User.objects.filter(email = posData['email'])
        if len(email_check) >= 1:
            errors['dups'] = "This Email is already taken"
        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    email= models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class appointManager(models.Manager):
    def appointval(self, postData, id):
        errors = []
        # print str(datetime.today()).split()[1]-> to see just the time in datetime
        
        
        if postData['date']:
            # if not postData["date"] >= unicode(date.today()):
            #     errors.append("Date must be set in future!")
            if len(postData["date"]) < 1:
                errors.append("Date field can not be empty")
            print("got to appointment post Data:", postData['date'])
        if len(postData['task'])<2:
            errors.append("Please insert take, must be more than 2 characters")
        if len(errors)==0:
            makeappoint= Appointment.objects.create(user=User.objects.get(id=id), task= postData['task'],date= str(postData['date']))
            return(True, makeappoint)
        else:
            return(False, errors)

    def edit_appointment(self, postData, app_id):
        errors = []
        print(errors)
        
        if postData["edit_date"] == "" or len(postData["edit_tasks"]) < 1:

            errors.append("All fields must be filled out!")
            print("all fields must fill out pop out")
        if errors == []:
            update_time= self.filter(id = app_id).update(task = postData['edit_tasks'], status = postData['edit_status'], date = postData['edit_date'])

            return (True, update_time)
        else:
            return (False, errors)

class Appointment(models.Model):
    user= models.ForeignKey(User, related_name="onrecord", on_delete = models.CASCADE)
    task= models.CharField(max_length=255)
    status= models.CharField(max_length=255)
    date= models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects= appointManager()