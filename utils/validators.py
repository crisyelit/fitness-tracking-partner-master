import os
from django.core.exceptions import ValidationError

def validate_file_track_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp3', '.wav', '.mp4', '.m4a']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validate_file_copyright_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.docx', '.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')