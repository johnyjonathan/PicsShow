from django.contrib import admin
from .models import UserImage

class UserImageAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(UserImage, UserImageAdmin)

