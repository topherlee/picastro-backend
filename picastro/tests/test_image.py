from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

def create_test_image():
    image_data = BytesIO()
    image = Image.new('RGB', (100, 100), 'white')
    image.save(image_data, format='png')
    image_data.seek(0)

    payload = {
        'img': SimpleUploadedFile("test.png", image_data.read(), content_type='image/png')
    }

