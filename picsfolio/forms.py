from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import ModelForm
from .models import UserImage, UserCatalog

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class uploadImgForm(ModelForm):
    class Meta:
        model = UserImage
<<<<<<< HEAD
        fields = ['name','image','description']
=======
        fields = ['name', 'image', 'description']
>>>>>>> 9f562577c471413145e1bba153a103dae70a4bee

class newCatalogForm(ModelForm):
    class Meta:
        model = UserCatalog
        fields = ['CatalogName']
<<<<<<< HEAD

class sort(ModelForm):
    class Meta:
        model = UserCatalog
        fields = ['CatalogName']
=======
>>>>>>> 9f562577c471413145e1bba153a103dae70a4bee
