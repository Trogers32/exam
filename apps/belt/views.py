from django.shortcuts import render, redirect
from django.contrib import messages
from apps.login_registration.models import *
from datetime import datetime, timedelta
import bcrypt
from django.core.urlresolvers import reverse

def home(request):
    try:
        uid = int(request.session['user_id'])
        uid = User.objects.get(id=uid)
        context = { 
            "user" : uid,
            "trips" : Trip.objects.filter(created_by=uid),
            "notme" : Trip.objects.exclude(created_by=uid).filter(users=uid),
            "other_trips" : Trip.objects.exclude(users=uid),
        }
        return render(request, "belt/index.html", context)
    except:
        return redirect('/')

def ctrip(request):
    try:
        uid = int(request.session['user_id'])
        context = {
            "user" : User.objects.get(id=uid),
        }
        return render(request, "belt/trip.html", context)
    except:
        return redirect('/')

def addtrip(request):
    try:
        uid = int(request.session['user_id'])
        uid = User.objects.get(id=uid)
        errors = Trip.objects.trip_validator(request.POST)
            # check if the errors dictionary has anything in it
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/trips/new")
        else:
            Trip.objects.create(destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], plan=request.POST['plan'], created_by=uid).users.add(uid)
            return redirect("/trips")
    except:
        return redirect('/')

def jointrip(request, num):
    try:
        uid = int(request.session['user_id'])
        uid = User.objects.get(id=uid)
        tip = int(num)
        Trip.objects.filter(id=tip).first().users.add(uid)
        return redirect("/trips")
    except:
        return redirect('/')

def canceltrip(request, num):
    try:
        uid = int(request.session['user_id'])
        uid = User.objects.get(id=uid)
        tip = int(num)
        Trip.objects.filter(id=tip).first().users.remove(uid)
        return redirect("/trips")
    except:
        return redirect('/')

def removetrip(request, num):
    try:
        uid = int(request.session['user_id'])
        uid = User.objects.get(id=uid)
        tip = int(num)
        Trip.objects.filter(id=tip).first().delete()
        return redirect("/trips")
    except:
        return redirect('/')

def edit_trip(request, num): ######################DO####
# try:
    uid = int(request.session['user_id'])
    u = User.objects.get(id=uid)
    t = Trip.objects.filter(id=num).first()
    if u == t.created_by:
        st = t.start_date
        st = datetime.strftime(st, '%Y-%m-%d')
        en = t.end_date
        en = datetime.strftime(en, '%Y-%m-%d')
        context = {
            "user" : User.objects.get(id=uid),
            "trip" : Trip.objects.filter(id=num).first(),
            "e" : en,
            "s" : st,
        }
        return render(request, "belt/edit.html", context)
    else:
        return redirect('/trips')
# except:
    return redirect('/')

def edit(request, num): ######################DO####
# try:
    uid = int(request.session['user_id'])
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/trips/edit/{num}")
    else:
        context = {
            "user" : User.objects.get(id=uid),
        }
        st = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
        en = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
        Trip.objects.filter(id=num).update(destination=request.POST['destination'], start_date=st, end_date=en, plan=request.POST['plan'])
        return redirect('/trips')
# except:
    return redirect('/')

def viewtrip(request, num):
    try:
        uid = int(request.session['user_id'])
        context = {
            "user" : User.objects.get(id=uid),
            "trip" : Trip.objects.filter(id=num).first(),
        }
        return render(request, "belt/desc.html", context)
    except:
        return redirect('/')