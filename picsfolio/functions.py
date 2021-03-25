import os
from PIL import Image
from PIL.ExifTags import TAGS

def getMetadataFromJpg(image_path):
    image=Image.open(image_path)
    exifdata = {}

    for tag, value in image._getexif().items():
       if tag in TAGS:
           exifdata[TAGS[tag]] = value
    return exifdata