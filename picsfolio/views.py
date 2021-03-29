from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserCreationForm, uploadImgForm
from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .models import UserImage
from .functions import getMetadataFromJpg, ROLimageId,RORimageId
from django.contrib import messages



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


    if request.method == 'GET':


        images = UserImage.objects.filter(user=request.user)
        return render(request,'picsfolio/loggedin.html', {'images':images})

    else:
        if request.POST.get("previous"):

            ROLimageId(request)
            images = UserImage.objects.filter(user=request.user)
            return render(request,'picsfolio/loggedin.html', {'images':images})

        elif request.POST.get("next"):

            RORimageId(request)
            images = UserImage.objects.filter(user=request.user)
            return render(request,'picsfolio/loggedin.html', {'images':images})

        elif request.POST.get("delete"):

            images = UserImage.objects.filter(user=request.user)
            ids = list(images.values_list('id', flat=True))
            if len(ids) != 0:
                UserImage.objects.get(id= ids[0]).delete()

            images = UserImage.objects.filter(user=request.user)

            return render(request,'picsfolio/loggedin.html', {'images':images})

    return redirect ('home')



def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect ('home')

def uploadimg(request):
    if request.method == 'GET':
        return render(request,'picsfolio/uploadimg.html', {'form': uploadImgForm()})
    else:
        form = uploadImgForm(request.POST, request.FILES)

        if not form.is_valid():
            if not bool(form.cleaned_data.get("name")):
                messages.info(request, 'Name field can not be empty.')
                return redirect ('uploadimg')
        elif form.cleaned_data.get("image") == 'default.jpg':
            messages.info(request, 'Image field can not be empty.')
            return redirect ('uploadimg')

        newimg = form.save(commit=False)
        newimg.user = request.user
        newimg.save()
        messages.info(request, 'Your picture has been uploaded successfully!')
        return redirect ('home')


def imgmetadata(request,image_id):
    img= get_object_or_404(UserImage, pk=image_id)
    exifdata = getMetadataFromJpg(img.image)
    return render(request,'picsfolio/imgmetadata.html', {'image':img,'exifdata':exifdata})