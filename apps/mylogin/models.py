from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def register(self, postdata):
        response = {}
        response['errors'] = []
        response['success'] = []
        dob = str(postdata['dob'])
        print dob
        if not postdata['email']:
            response['errors'].append('Email is blank')
        if not EMAIL_REGEX.match(postdata['email']):
            response['errors'].append('Not a valid email address')
        if not postdata['name']:
            response['errors'].append('name is blank')
        if not postdata['alias']:
            response['errors'].append('alias is blank')
        if not postdata['password']:
            response['errors'].append('Password is blank')
        if len(postdata['password'])<8:
            response['errors'].append('Password is less than 8 characters')
        if postdata['password'] != postdata['confirmpw']:
            response['errors'].append('Password does not match')
        if not postdata['dob']:
            response['errors'].append('please add your date of birth')
        if not response['errors']:
            password = postdata['password']
            password = password.encode()
            hashedpw = bcrypt.hashpw(password, bcrypt.gensalt())
            try: 
                newuser = Users.objects.create(name = postdata['name'], alias = postdata['alias'], email = postdata['email'],password = hashedpw)
                response['success'].append('Registered User')
                print 'User Created'
                return response
            except:
                response['errors'].append('Unable to add to DB')
                return response
        else:
            return response

    def login(self, postdata):
        response = {}
        response['errors'] = []
        response['success'] = []
        try: 
            print 'trying get'
            user = Users.objects.get(email = postdata['email'])
            print 'try worked'
        except:
            response['errors'].append('email not found')
            return response
        password = postdata['password']
        password = password.encode()
        hashedpw = user.password
        hashedpw = hashedpw.encode()
        print 'password encoded'
        if bcrypt.hashpw(password, hashedpw) == hashedpw:
            response['success'].append('login successful')
            print 'matched hash'
            return response
        else:
            response['errors'].append('passwords do not match')
            return response
        
    def allusersminusyou(self, userid):
        you = Users.objects.get(id=userid)
        allusers = Users.objects.all().exclude(id=userid)
        return allusers
        
class Users(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=50, unique=True)
    dob = models.DateField(default = datetime.datetime.now().date())
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()