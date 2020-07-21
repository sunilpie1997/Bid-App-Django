from rest_framework.parsers import FileUploadParser

class ImageUploadParser(FileUploadParser):
    media_type='image/*'
