from django.db import models
from django.contrib.auth.models import User

from PIL import Image
from PIL.ExifTags import TAGS

from fractions import Fraction


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

    def imageList(catalogName, request):

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


class UserImage(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="piscfolio/images", default='default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    catalog = models.ForeignKey(UserCatalog, on_delete=models.CASCADE, default='1')
    description = models.TextField(blank=True, max_length='1000')



    def __str__(self):
        return self.name
