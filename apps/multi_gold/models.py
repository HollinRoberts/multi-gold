# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import random
NAME = re.compile(r'^[a-zA-Z\s]*$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD = re.compile(r'[A-Za-z0-9]{8,}')
DATE= re.compile(r'^(0[1-9]|1[0-2])\/(0[1-9]|1\d|2\d|3[01])\/(19|20)\d{2}$')

class UserManager(models.Manager):
    def email_check(self,postData):
        try:
            email=postData['email']
            user=User.objects.filter(email=email)
            user[0].email==email
            return True
        except:
            return False
    
    def basic_validator(self, postData):
        errors = {}
        if User.objects.email_check(postData):
            errors["user"]="User already exists"
        print postData
        if len(postData['name'])<2:
            errors['name']="Please enter a name."
        elif not NAME.match(postData['name']):
            errors['name']="Name can only have letters."
        if len(postData['email'])==0:
            errors['email']="Please enter an email."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email2']="Improper Email"
        if postData['password']!=postData['confirm']:
            errors['password']="Passwords don't match"
        if not PASSWORD.match(postData['password']):
            errors['password']="Password must have an upercase and lowercase leter, a number and be a minimum of 8 characters."
        return errors;

    def login(self,postData,request):
        email=postData['email']
        user=User.objects.filter(email=email)
        password=postData['password']
        try:
            user_password=user[0].password
            if User.objects.email_check(postData) and bcrypt.checkpw(password.encode(),user_password.encode()):
                request.session['id']=user[0].id
                print request.session['id']
                request.session['name']=user[0].name
                print request.session['name']
                return True
        except:
            return False
    
    def user_creation(self,postData,request):
        name=postData['name']
        email=postData['email']
        gold=0
        password=postData['password']
        password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        created=User.objects.create(name=name,email=email,password=password,gold=gold)
        request.session['id']=created.id
        print request.session['id']
        return self;

    def login_check(self,request):
        try:
            temp = request.session['id']
            print request.session['id']
        except:
            print "no id"
            return False
        return True

    def gold_check(self,request):
        userid=request.session['id']
        user=User.objects.get(id=userid)
        print user.name
        print '*'
        print user.gold 
        temp=user.gold
        if temp<0:
            return True
        else:
            return False

            

class ActionsManager(models.Manager):
    def action_calc(self,request,postData):
        if 'cave' in postData:
            location='cave'
            amount = random.randrange(-5,5)
            if amount<0:
                result='lost'
            else:
                result='gained'
        if 'castle' in postData:
            location='castle'
            amount = random.randrange(-10,10)
            if amount<0:
                result='lost'
            else:
                result='gained'
        if 'farm' in postData:
            location='farm'
            amount = random.randrange(-1,1)
            if amount<0:
                result='lost'
            else:
                result='gained'
        print amount
        user=User.objects.get(id=request.session['id'])
        gold= user.gold
        print gold
        gold+=amount
        print gold
        user.gold=gold
        print user.gold
        user.save()
        action= Actions.objects.create(place=location,result=result,amount=amount,users_action=User.objects.get(id=request.session['id'])) 
        print action.users_action.name
        return self 


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    gold = models.IntegerField()
    email = models.CharField(max_length=255,null=True)
    def __repr__(self):
        return "<User object: {} {} {}>".format(self.name, self.password, self.gold)
    objects = UserManager()

class Actions(models.Model):
    place = models.CharField(max_length=20)
    result = models.CharField(max_length=20)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    users_action = models.ForeignKey(User, related_name = "actions_taken")
    def __repr__(self):
        return "<Actions object: {} {} {} {}>".format(self.place, self.result, self.amount, self.users_action)
    objects = ActionsManager()