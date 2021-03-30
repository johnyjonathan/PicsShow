import os
from PIL import Image
from PIL.ExifTags import TAGS
from .models import UserImage

def getMetadataFromJpg(image_path):
    image=Image.open(image_path)

    exifdata = image.getexif()
    metadata = []

    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        metadata.append(f"{tag} : {data}")

    exifdata = metadata

    if len(exifdata) == 0:
        exifdata = "The file does not contain any metadata."

    return exifdata


def ROLimageId(request):

    images = UserImage.objects.filter(user=request.user)
    ids = list(images.values_list('id', flat=True))
    if len(ids) == 0:
        return

    idsh = ids[:]
    idsh.append(idsh.pop(0)) #obrót listy id w lewo o 1

    for i in range(len(ids)):
        image = UserImage.objects.get(user=request.user, id= ids[i])
        image.id = idsh[i]+100
        image.save()
        UserImage.objects.get(user=request.user, id= ids[i]).delete()

def RORimageId(request):

    images = UserImage.objects.filter(user=request.user)
    ids = list(images.values_list('id', flat=True))
    if len(ids) == 0:
        return
    idsh = ids[:]
    idsh.insert(0,idsh.pop(-1)) #obrót listy id w prawo o 1

    for i in range(len(ids)):
        image = UserImage.objects.get(user=request.user, id= ids[i])
        image.id = idsh[i]+100
        image.save()
        UserImage.objects.get(user=request.user, id= ids[i]).delete()