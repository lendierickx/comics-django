import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from inventory_setting.forms.userform import UserForm


def ajax_register(request):
    """
        Function provides user registration into our system. Any user that wants
        to log in using username / passwords is going to have to be registered
        by this function.
    """
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            form = UserForm(request.POST)
            # Validate the form: the captcha field will automatically
            # check the input
            if form.is_valid():
                response_data = create_user(form)  # Create our store
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    else:
        response_data = {'status' : 'failure', 'message' : 'Not acceptable request made.' }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def create_user(form):
    # Perform validation to ensure the email/username are unique.
    email = form['email'].value().lower()
    try:
        user = User.objects.get(email=email)
        return {'status' : 'failure', 'message' : 'email already exists! Please choose a unique email.' }
    except User.DoesNotExist:
        pass
    
    # Perform validation to avoid blank passwords and mismatched passwords.
    if form['password'].value() != form['password_repeated'].value():
        print("pass1", form['password'].value())
        print("pass2", form['password_repeated'].value())
        return {'status' : 'failure', 'message' : 'Entered passwords do not match.'}
    if form['password'].value() is '' or form['password_repeated'].value() is '':
        return {'status' : 'failure', 'message' : 'blank passwords are not acceptable' }

    # Create the user in our database

    try:
        user = User.objects.create_user(
            email,  # Username
            email,  # Email
            form['password'].value(),
        )
        user.first_name = form['first_name'].value()
        user.last_name = form['last_name'].value()
        # user.is_active = False;  # Need email verification to change status.
        user.save()
    except Exception as e:
        return {
            'status' : 'failure',
            'message' : 'An unknown error occured, failed registering user.'
        }

    # Return success status
    return {
        'user_id': user.id,
        'status' : 'success',
        'message' : 'user registered'
    }


@login_required()
def ajax_update_password(request):
    response_data = {'status' : 'failed', 'message' : 'unknown deletion error'}
    if request.is_ajax():
        if request.method == 'POST':
            old_password = request.POST['old_password']
            password = request.POST['password']
            repeat_password = request.POST['password_repeated']
            
            # Validate password.
            if request.user.check_password(old_password) == False:
                response_data = {'status' : 'failure', 'message' : 'invalid old password' }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if password is '' or request is '':
                response_data = {'status' : 'failure', 'message' : 'blank passwords are not acceptable' }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if password != repeat_password:
                response_data = {'status' : 'failure', 'message' : 'passwords do not match' }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            
            # Update model
            request.user.set_password(password)
            request.user.save()
        
        response_data = {'status' : 'success', 'message' : 'updated password'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")