import io, os
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from djangoAngular.mixins import UpdateableMixin, SlugeableMixin
from django.utils import timezone


class ResponsiveImage(UpdateableMixin, SlugeableMixin):
    type = models.CharField(max_length=250, default=None, blank=True)
    author = models.CharField(max_length=250, default=None, blank=True)
    caption = models.CharField(max_length=100, default=None, blank=True)
    alt = models.CharField(max_length=100, default=None, blank=True)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to='images/',
        blank=False,
    )
    thumbnail = models.ImageField(
        upload_to='images/',
        default=None,
        blank=True
    )
    tablet = models.ImageField(
        upload_to='images/',
        default=None,
        blank=True
    )
    desktop = models.ImageField(
        upload_to='images/',
        default=None,
        blank=True
    )

    def save(self):
        if not self.slug:
            self.slug = self.get_unique_slug()

        image = Image.open(io.BytesIO(self.image.read()))

        self.remove_previous()

        self.width, self.height = image.size
        self.image.save(
            name=self.rename(),
            content=self.resize(image, max(self.width, self.height)),
            save=False
        )

        self.thumbnail.save(
            name=self.rename('-thumbnail'),
            content=self.resize(image, 800, 192),
            save=False
        )

        self.tablet.save(
            name=self.rename('-tablet'),
            content=self.resize(image, 1600, 192),
            save=False
        )

        self.desktop.save(
            name=self.rename('-desktop'),
            content=self.resize(image, 2800, 192),
            save=False
        )

        super(ResponsiveImage, self).save()

    def rename(self, extra_string=''):
        return self.slug + extra_string + '.jpg'

    def remove_previous(self):
        if self.thumbnail.name and not self.image.name in self.thumbnail.name:
            if os.path.isfile(self.thumbnail.path):
                os.remove(self.thumbnail.path)
                os.remove(self.thumbnail.path.replace('-thumbnail', ''))
                os.remove(self.thumbnail.path.replace('-thumbnail', '-tablet'))
                os.remove(self.thumbnail.path.replace('-thumbnail', '-desktop'))

    def resize(self, image, edge, dpi=72):
        content = io.BytesIO()
        image.resize(self.scale(edge), Image.ANTIALIAS).save(fp=content, format='JPEG', dpi=[dpi, dpi])
        return ContentFile(content.getvalue())

    def scale(self, long_edge):
        if self.width > self.height:
            ratio = long_edge * 1. / self.width
        else:
            ratio = long_edge * 1. / self.height
        return int(self.width * ratio), int(self.height * ratio)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

