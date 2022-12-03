from email.policy import default

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.


class Sector(models.Model):
    name = models.CharField(max_length=65)  # charfild = varchar

    def __str__(self):
        return self.name

class ImpressoraDeth(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    serial = models.CharField(max_length=100)

    def __str__(self):
        return self.modelo

class Priority(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AppliedSolution(models.Model):
    name = models.CharField(max_length=50)
    modelo = models.ForeignKey(ImpressoraDeth, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Called(models.Model):
    title = models.CharField(max_length=65)  # charfild = varchar
    user_requester = models.CharField(max_length=50)
    priority = models.ForeignKey(
        Priority, on_delete=models.SET_NULL, null=True
    )
    slug = models.SlugField(unique=False)
    call_defect = models.TextField()
    description = models.TextField()
    pendencies = models.TextField()
    created_at = models.DateTimeField()
    is_resolved = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='calleds/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Sector, on_delete=models.SET_NULL, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    appliedsolution = models.ForeignKey(
        AppliedSolution, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)