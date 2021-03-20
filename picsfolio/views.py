from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def home(request):
    return render(request,'picsfolio/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request,'picsfolio/loginuser.html',{'form':AuthenticationForm()} )
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'picsfolio/loginuser.html',{'form':AuthenticationForm(), 'error':'Username or password did not match'})
        else:
            login(request, user)
            return redirect('loggedin')


def signupuser(request):
    if request.method == 'GET':
        return render(request,'picsfolio/signupuser.html',{'form':UserCreationForm()} )
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], email=request.POST['email'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('loggedin')
            except IntegrityError:
                return render(request,'picsfolio/signupuser.html',{'form':UserCreationForm(), 'error':'That username has already taken'})
        else:
            return render(request,'picsfolio/signupuser.html',{'form':UserCreationForm(), 'error':'Passwords did not match'} )

def loggedin(request):
    return render(request,'picsfolio/loggedin.html')



def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect ('home')
    