import os
from PIL import Image
from PIL.ExifTags import TAGS
from .models import UserImage, UserCatalog

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


def rotateImageId(request, catalogName, shift):


    if catalogName == "All":
        images = UserImage.objects.filter(user=request.user)
    else:
        CurrentCatalog = UserCatalog.objects.get(user=request.user, CatalogName=catalogName)
        images = UserImage.objects.filter(user=request.user, catalog=CurrentCatalog)

    ids = list(images.values_list('id', flat=True))
    if len(ids) == 0:
        return

    ids2 = ids[:]

    if shift > 0:
        for i in range(shift):
            ids2.append(ids2.pop(0))        # obrót listy id w lewo o 1
    elif shift < 0:
        for i in range(-shift):
            ids2.insert(0, ids2.pop(-1))    # obrót listy id w prawo o 1
    else:
        return

    for i in range(len(ids)):
        image = UserImage.objects.get(user=request.user, id= ids[i])
        image.id = ids2[i]+10000
        image.save()
        UserImage.objects.get(user=request.user, id= ids[i]).delete()

    for i in range(len(ids2)):
        image = UserImage.objects.get(user=request.user, id= ids[i]+10000)
        image.id = ids[i]
        image.save()
        UserImage.objects.get(user=request.user, id= ids[i]+10000).delete()

    return

