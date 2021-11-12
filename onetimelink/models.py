from django.db import models

# Create your models here.
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from . import presettings
from . import api

import os


class DownloadSite(models.Model):
    class Meta:
        verbose_name = 'Download Site'
    link_key = models.CharField(max_length=63, editable=False, unique=True)
    timestamp_creation = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        editable=False,
        verbose_name=_(u'creation time'),
    )

    def save(self, * args, ** kwargs):
        """Perform custom methods before saving."""
        # If not available set a link key before saving
        if not self.link_key:
            self.link_key = api.gen_key()

        # call the real save method
        try:
            super(DownloadSite, self).save(*args, ** kwargs)
        except IntegrityError:
            # enforce a unique key (with a longer string)
            import time
            key = str(time.time()).replace('.', '')
            self.link_key = key + api.gen_key()
            # call the save method again
            super(DownloadSite, self).save(*args, ** kwargs)

    def __str__(self):
        return self.link_key


class UploadFile(models.Model):
    class Meta:
        verbose_name = 'Upload File'
    display_name = models.CharField(max_length=63, blank=False, null=False, unique=True, verbose_name=_('Display Name'))
    file = models.FileField(
        upload_to=presettings.DYNAMIC_LINK_UPLOAD_TO,
        help_text=_(u'Select the file to upload'),
        verbose_name=_(u'file'),
        max_length=255,
    )

    def __str__(self):
        return self.display_name


class Download(models.Model):
    active = models.BooleanField(default=True, verbose_name=_(u'is active'))
    link_key = models.CharField(max_length=63, editable=False, unique=True)
    timestamp_creation = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        editable=False,
        verbose_name=_(u'creation time'),
    )
    site = models.ForeignKey(DownloadSite, models.CASCADE, related_name='downloads', blank=True, null=True)
    down_file = models.ForeignKey(UploadFile, models.CASCADE, related_name='downloads', blank=True, null=True)

    def get_filename(self):
        return os.path.basename(self.down_file.file.path)

    def get_path(self):
        """
        if active it returns the full path of stored file to serve.
        if clicked it returns None
        """
        if self.active:
            self.active = False
            self.save()
            return self.down_file.file.path
        return None

    def save(self, * args, ** kwargs):
        """Perform custom methods before saving."""
        # If link not created, generate a link key before saving
        if not self.link_key:
            self.link_key = api.gen_key()

        # call the real save method
        try:
            super(Download, self).save(*args, ** kwargs)
        except IntegrityError:
            # enforce a unique key (with a longer string)
            import time
            key = str(time.time()).replace('.', '')
            self.link_key = key + api.gen_key()
            # call the save method again
            super(Download, self).save(*args, ** kwargs)

    def __unicode__(self):
        if self.down_file is not None:
            return '%s: %s, %s' % (
                str(_(u'Filename')),
                self.down_file.display_name,
                self.get_filename()
            )
        else:
            return '%s: %s' % (
                str(_(u'Filename')),
                self.get_filename()
            )

    def __str__(self):
        if self.down_file is not None:
            return 'Name: %s  Key: %s  Path: %s' % (self.down_file.display_name, self.link_key, self.down_file.file.path)
        else:
            return self.link_key


class IsExpiredError(Exception):
    """Error class for expired link objects"""

    def __init__(self, value=''):
        self.value = presettings.TEXT_REQUEST_IS_EXPIRED + value

    def __str__(self):
        return repr(self.value)
