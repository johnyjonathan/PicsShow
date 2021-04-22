from django.db import models
from django.contrib.auth.models import User

from PIL import Image
from PIL.ExifTags import TAGS

from fractions import Fraction
from natsort import natsorted

class imagesMetadataList:
    def __init__(self, DateTimeOriginal, Model, ExposureTime,FNumber, ISOSpeedRatings, LensModel,View):
        self.DateTimeOriginal = DateTimeOriginal
        self.Model = Model
        self.ExposureTime = ExposureTime
        self.FNumber = FNumber
        self.ISOSpeedRatings = ISOSpeedRatings
        self.LensModel = LensModel
        self.View = View


class UserCatalog(models.Model):
    CatalogName = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1')

    def __str__(self):
        return self.name

    def createImageList(catalogName, request):

        images = []

        if catalogName == "All":
            imagesNames = UserImage.objects.filter(user=request.user).values_list('name', flat=True)
        else:
            imagesNames = UserCatalog.objects.get(user=request.user, CatalogName=catalogName).userimage_set.all()


        for IMGname in imagesNames:

            imageA = UserImage.objects.get(name=IMGname,user=request.user)
            imageFile = Image.open(imageA.image)
            exifData = imageFile.getexif()
            metadata = {}

            for tag_id in exifData:
                tag = TAGS.get(tag_id, tag_id)
                data = exifData.get(tag_id)
                metadata[f"{tag}"] = f"{data}"

            nodata = "None"

            try:
                DateTimeOriginal = metadata["DateTimeOriginal"]
            except:
                DateTimeOriginal = nodata
            try:
                Model = metadata["Model"]
            except:
                Model = nodata
            try:
                ExposureTime = str(Fraction(float(metadata["ExposureTime"])).limit_denominator())
            except:
                ExposureTime = nodata
            try:
                FNumber = metadata["FNumber"]
            except:
                FNumber = nodata
            try:
                ISOSpeedRatings = metadata["ISOSpeedRatings"]
            except:
                ISOSpeedRatings = nodata
            try:
                LensModel = metadata["LensModel"]
            except:
                LensModel = nodata

            imgMetadataList=imagesMetadataList(DateTimeOriginal, Model, ExposureTime,FNumber, ISOSpeedRatings, LensModel, True)

            images.append([imageA, imgMetadataList])

            if request.method != 'GET' and not request.POST.get("Select"):
                imagesToShow = list(request.POST.getlist("showCheckbox"))
                for image, MDlist in images:
                    if image.name in imagesToShow:
                        MDlist.View = True
                    else:
                        MDlist.View = False

        return images

    def sortImages(request, imagesList, SortParameter):


        lista = []

        for image, MD in imagesList:
            if SortParameter == 'Name':
                lista.append([image.name, image.id])
            if SortParameter == 'DateTimeOriginal':
                lista.append([MD.DateTimeOriginal, image.id])
            if SortParameter == 'Model':
                lista.append([MD.Model, image.id])
            if SortParameter == 'ExposureTime':
                lista.append([MD.ExposureTime, image.id])
            if SortParameter == 'FNumber':
                lista.append([MD.FNumber, image.id])
            if SortParameter == 'ISOSpeedRatings':
                lista.append([MD.ISOSpeedRatings, image.id])
            if SortParameter == 'LensModel':
                lista.append([MD.LensModel, image.id])

        ids = []

        for x, y in lista:
            ids.append(y)

        if SortParameter == 'Name':
            lista.sort(key=lambda y: y[0].lower())
        else:
            lista = natsorted(lista, key=lambda y: y[0])

        ids2 = []

        for x, y in lista:
            ids2.append(y)

        if ids == ids2:
            ids.reverse()

        for i in range(len(ids)):
            image = UserImage.objects.get(user=request.user, id=ids2[i])
            image.id = ids[i] + 10000
            image.save()
            UserImage.objects.get(user=request.user, id=ids2[i]).delete()

        for i in range(len(ids2)):
            image = UserImage.objects.get(user=request.user, id=ids[i] + 10000)
            image.id = ids[i]
            image.save()
            UserImage.objects.get(user=request.user, id=ids[i] + 10000).delete()

        return


class UserImage(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="piscfolio/images", default='default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    catalog = models.ForeignKey(UserCatalog, on_delete=models.CASCADE, default='1')
    description = models.TextField(blank=True, max_length='1000')


    def __str__(self):
        return self.name

    def getMetadataFromJpg(image_path):

        image = Image.open(image_path)

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
