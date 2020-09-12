from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


class PicturesUsersS3Boto3Storage(S3Boto3Storage):
    location = "media/pictures"
    file_overwrite = False
