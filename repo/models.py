from django.db import models
from django.utils import timezone
from fire.settings import AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser
from repo.helpers import get_category_choices_mapped
from PIL import Image


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(
        default="default.jpg", upload_to='profile-images', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# Create your models here.
'''
Each user will have a default Folder with no name, and has the is_root value of true
'''


class Folder(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="folders")
    name = models.CharField(max_length=64, blank=False)
    is_root = models.BooleanField(default=False)

    # Experimental, can be implemented if we have enough time
    is_shared = models.BooleanField(default=False)

    def __str__(self):
        return self.name


'''
A folder, if not is_root should have an heir data with it as the "folder"
It will relate itself to a folder which it will refer to as its "parent"

'''


class HeirData(models.Model):
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="parents")
    parent = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="children")


class File(models.Model):
    category_choices = get_category_choices_mapped()
    name = models.CharField(max_length=255, blank=False)
    category = models.CharField(
        max_length=64, blank=False, choices=category_choices)
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="files")
    uploaded_at = models.DateTimeField(default=timezone.now)
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to='')

    def __str__(self):
        return self.file.name
