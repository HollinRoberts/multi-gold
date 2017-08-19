# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from models import User, Actions, UserManager

def index(request):
    print "index"
    return render(request, 'multi_gold/login.html')

def dashboard(request):
    print "dashboard"
    if User.objects.gold_check(request):
        return redirect('/delete')
    if User.objects.login_check(request):
        top_five = User.objects.raw('SELECT id, name, gold FROM multi_gold_User ORDER BY gold DESC')
    
        context={"top_five":top_five, "range":range(5)}
        return render(request, 'multi_gold/dashboard.html',context)
    else:
        return redirect('/')

def user(request,name):
    print "user"
    print name
    if User.objects.gold_check(request):
        return redirect('/delete')
    if User.objects.login_check(request):
        userid=User.objects.filter(name=name)[0].id
        print userid
        context={'user':User.objects.filter(name=name),'actions':User.objects.get(id=userid).actions_taken.all()}
        return render(request, 'multi_gold/user.html',context)
    else:
        return redirect('/')

def gold(request):
    print "gold"
    if User.objects.gold_check(request):
        return redirect('/delete')
    if User.objects.login_check(request):
        context={'actions':User.objects.get(id=request.session['id']).actions_taken.all()}
        return render(request, 'multi_gold/gold.html', context)
    else:
        return redirect('/')

def leaderboard(request):
    print "leaderboard"
    if User.objects.gold_check(request):
        return redirect('/delete')
    if User.objects.login_check(request):
        top_five = User.objects.raw('SELECT id, name, gold FROM multi_gold_User ORDER BY gold DESC')
        context={"top_five":top_five, "range":range(5)}
        return render(request, 'multi_gold/leaderboard.html',context)
    else:
        return redirect('/')

def log_out(request):
    print "logout"
    return redirect('/')

def login(request):
    print "login"
    if User.objects.login(request.POST,request):
        print 'in if in login'
        return redirect('/dashboard')
    else:
        print 'login redirect'
        return redirect('/')

def register(request):
    print "register"
    errors = User.objects.basic_validator(request.POST)
    print errors
    if len(errors):
        for tag, error in errors.iteritems():
            print "errors"
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        print 'in submit else'
        User.objects.user_creation(request.POST,request)
        return redirect('/dashboard')

def action(request):
    print "action"
    if User.objects.gold_check(request):
        print "in gold check if"
        return redirect('/delete')
    else:
        Actions.objects.action_calc(request,request.POST)
        return redirect('/gold')

def delete(request):
    temp=request.session['id']
    User.objects.get(id=temp).delete()
    request.session.flush()
    return HttpResponse ('You, are out of gold')