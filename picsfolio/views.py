from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserCreationForm, uploadImgForm, newCatalogForm
from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .models import UserImage, UserCatalog
from .functions import getMetadataFromJpg, rotateImageId
from django.contrib import messages

tiles = True

def home(request):

    return render(request, 'picsfolio/home.html')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'picsfolio/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'picsfolio/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username or password did not match'})
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
            return render(request,'picsfolio/signupuser.html',{'form':UserCreationForm(), 'error': 'Passwords did not match'} )


def loggedin(request):

    catalogs = UserCatalog.objects.filter(user=request.user).values_list('CatalogName', flat=True)
    images = UserCatalog.imageList("All", request)

    if request.method == 'GET':
        return render(request, 'picsfolio/loggedin.html', {'images': images, 'catalogs': catalogs})
    else:
        catalogName = request.POST.get("Catalogs")
        imageView = request.POST.get("radio-view")

        global tiles

        print(imageView)


        if imageView == "list":
            tiles = False
        elif imageView == "tiles":
            tiles = True
        else:
            if tiles == True:
                imageView = "Tiles"
            else:
                imageView = "list"

        print(imageView)


        images = UserCatalog.imageList(catalogName, request)


        if request.POST.get("Select"):
            return render(request, 'picsfolio/loggedin.html', {'images': images, 'catalogs': catalogs, 'selected': catalogName, 'imageView' : imageView})

        if request.POST.get("previous"):

            rotateImageId(request, catalogName, 1)
            images = UserCatalog.imageList(catalogName, request)
            return render(request, 'picsfolio/loggedin.html', {'images': images, 'catalogs': catalogs,'selected': catalogName, 'imageView' : imageView})

        elif request.POST.get("next"):

            rotateImageId(request, catalogName, -1)
            images = UserCatalog.imageList(catalogName, request)
            return render(request, 'picsfolio/loggedin.html', {'images': images, 'catalogs': catalogs,'selected': catalogName, 'imageView' : imageView})

        elif request.POST.get("delete"):

            ids = []
            for image, MD in images:
                ids.append(image.id)

            if len(ids) != 0:
                UserImage.objects.get(id=ids[0]).delete()

            images = UserCatalog.imageList(catalogName, request)
            return render(request, 'picsfolio/loggedin.html', {'images': images, 'catalogs': catalogs,'selected': catalogName, 'imageView' : imageView})

        elif request.POST.get("imagePreview"):
            ids = []
            for image, MD in images:
                ids.append(image.id)
            shift = ids.index(int(request.POST.get("imagePreview")))
            rotateImageId(request, catalogName, -shift)
            images = UserCatalog.imageList(catalogName, request)

            return render(request, 'picsfolio/loggedin.html', {'images': images, 'catalogs': catalogs,'selected': catalogName, 'imageView' : imageView})

    return render(request, 'picsfolio/loggedin.html', {'images': images, 'catalogs': catalogs,'selected': catalogName, 'imageView' : imageView})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def uploadimg(request):

    catalogs = UserCatalog.objects.filter(user=request.user).values_list('CatalogName', flat=True)

    if request.method == 'GET':
        return render(request,'picsfolio/uploadimg.html', {'form': uploadImgForm(), "catalogs": catalogs})
    else:
        form = uploadImgForm(request.POST, request.FILES)
        CatalogForm = newCatalogForm(request.POST)

        if request.POST.get("upload"):
            if not form.is_valid():
                if not bool(form.cleaned_data.get("name")):
                    messages.info(request, 'Name field can not be empty.')
                    return redirect('uploadimg')
            elif form.cleaned_data.get("image") == 'default.jpg':
                messages.info(request, 'Image field can not be empty.')
                return redirect('uploadimg')

            if not bool(request.POST.get("catalog")):
                messages.info(request, 'Choose catalog.')
                return redirect('uploadimg')

            chosenCatalogName = request.POST.get("catalog")
            newimg = form.save(commit=False)
            newimg.user = request.user
            newimg.catalog = UserCatalog.objects.get(CatalogName=chosenCatalogName)
            newimg.save()

            messages.info(request, 'Your picture has been uploaded successfully!')

            return render(request,'picsfolio/uploadimg.html', {'form': uploadImgForm(), "catalogs": catalogs, "chosenCatalogName" : chosenCatalogName})

        elif request.POST.get("AddCatalog"):

            if not bool(request.POST.get("CatalogName")):
                messages.info(request, 'Catalog name field can not be empty!')
            elif not request.POST.get("CatalogName") in catalogs:
                newCatalog = CatalogForm.save(commit=False)
                newCatalog.user = request.user
                newCatalog.save()
            else:
                messages.info(request, 'Catalog name must be unique!')

        return redirect('uploadimg')


def imgmetadata(request, image_id):
    img = get_object_or_404(UserImage, pk=image_id)
    exifdata = getMetadataFromJpg(img.image)
    return render(request, 'picsfolio/imgmetadata.html', {'image': img, 'exifdata': exifdata})
