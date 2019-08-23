from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
import bcrypt
import pytz
from validate_email import validate_email
import re


class User_validation(models.Manager):   
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters long."
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last name should be at least 2 characters long."
        if User.objects.filter(email=postData['email']).first():
            errors["email"] = "Email already registered."
        elif postData['email'] == '':
            errors["email"] = "Email can't be blank."
        else:
            is_valid = validate_email(postData['email'])
            if is_valid == False:
                errors["email"] = "Invalid email."
            elif not re.match(r"[^@]+@[^@]+\.[^@]+",postData['email']):
                errors["email"] = "Invalid email."
        if len(postData['password']) < 8:
            errors["password"] = "Password needs to be at least 8 characters long."
        elif postData['password'] != postData['confirm_password']:
            errors["password"] = "Passwords do not match."
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            logged_user = user[0] 
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors['pword'] = "Incorrect email or password."
        else:
            errors['pword'] = "Incorrect email or password."
        return errors

class Trip_validation(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 3:
            errors["destination"] = "Trip destination must be at least 3 characters."
        if postData['start_date'] == '':
            errors["start"] = "Must have a start date."
        else:
            # st = datetime.strptime(postData['start_date'], '%b. %d, %Y')
            # st = datetime.strftime(st, '%Y-%m-%d')
            # st = datetime.strptime(st, '%Y-%m-%d')
            st = datetime.strptime(postData['start_date'], '%Y-%m-%d')
            if st < datetime.today():
                errors["start"] = "Start date should be in the future."
        if postData['end_date'] == '':
            errors["end"] = "Must have an end date."
        else:
            # en = datetime.strptime(postData['end_date'], '%b. %d, %Y')
            # en = datetime.strftime(en, '%Y-%m-%d')
            # en = datetime.strptime(en, '%Y-%m-%d')
            en = datetime.strptime(postData['end_date'], '%Y-%m-%d')
            if en < st:
                errors["end"] = "End date should be after the start date."
            if en < datetime.today():
                errors["fend"] = "End date should be in the future."
        if len(postData['plan']) < 3:
            errors["plan"] = "Trip plan must be at least 3 characters."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_validation()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="my_trip")
    users = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Trip_validation()