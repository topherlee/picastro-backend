import os
from pgmagick import Image, FilterTypes

from picastro_backend.settings import BASE_DIR


def img_scale(image_url):
    im = Image(str(image_url))
    im.quality(100)
    im.scale('1000x1000')
    im.sharpen(1.0)
    #im.write(str(BASE_DIR / 'media/resize/kaboom-scale.jpg'))
    im.write(str(BASE_DIR / 'media/resize') + '/' + 'scale' + image_uri.split("/")[-1])


def img_resize(image_url):
    im = Image(str(image_url))
    im.filterType(FilterTypes.SincFilter)
    im.resize('1000x1000')
    #im.write(str(BASE_DIR / 'media/resize/kaboom-resize.jpg'))
    im.write(str(BASE_DIR / 'media/resize') + '/' + 'resize_' + image_uri.split("/")[-1])


#image_source = 'media/images/kaboom.jpg'

#img_scale(BASE_DIR / 'media/images/kaboom.jpg')
#img_resize(BASE_DIR / 'media/images/kaboom.jpg')

#img_scale(BASE_DIR / 'media/images/IMG_5364.TIF')
#img_resize(BASE_DIR / 'media/images/IMG_5364.TIF')



def create_list_of_imagefiles():
    # search folder to create a list of all json-files in that folder
    list_of_image_files = []
    for x in os.listdir(BASE_DIR / 'media/test_images/'):
        list_of_image_files.append(x)
    print(list_of_image_files)
    return list_of_image_files



list_of_images = create_list_of_imagefiles()
for image in list_of_images:
    image_uri = str(BASE_DIR) + '/media/test_images/' + image
    print(image_uri)
    #print(image_uri.split("/")[-1])
    #print(str(BASE_DIR / 'media/resize') + '/' + image_uri.split("/")[-1])
    img_scale(image_uri)
    img_resize(image_uri)
