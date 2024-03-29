from datetime import datetime
from email.policy import default

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

class Pass_point(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField()
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.author

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
    ch_y_n = (
        ('Sim','Sim'),
        ('Não', 'Não'),
    )
    is_resolved = models.CharField(choices=ch_y_n, max_length=10)
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

    def get_created_at(self):
        return self.created_at.strftime('%d/%m/%y %H:%M Hrs')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)