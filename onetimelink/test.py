from django.test import TestCase
from django.core.files import File

from onetimelink.models import UploadFile, Download, DownloadSite
from onetimelink.api import file_link_url, site_link_url
from onetimelink import presettings

import os

class Obj:
    pass


class UploadFileCase(TestCase):
    def setUp(self):
        f = open(os.getcwd() + '/media/pier-569314_640.jpg', 'rb')
        UploadFile.objects.create(display_name="test", file=File(f))

    def test_uploaded_file(self):
        down_file = UploadFile.objects.all().last()

        # Clean uploaded file
        os.remove(down_file.file.path)

        self.assertEqual(down_file.display_name, 'test')


class DownloadCase(TestCase):
    def setUp(self):
        f = open(os.getcwd() + '/media/pier-569314_640.jpg', 'rb')
        UploadFile.objects.create(display_name="test", file=File(f))

    def test_download(self):
        down_file = UploadFile.objects.all().last()

        # Clean uploaded file
        os.remove(down_file.file.path)

        d = Download(down_file=down_file)
        d.save()
        self.assertEqual(d.get_path(), d.down_file.file.path)
        request = Obj()
        request.__dict__['META'] = {}
        request.META['HTTP_HOST'] = 'www.example.com'
        link = '%s%s/%s/link/%s/%s' % (
            'http://',
            request.META.get('HTTP_HOST'),
            presettings.DYNAMIC_LINK_URL_BASE_COMPONENT,
            d.link_key,
            d.get_filename()
        )
        self.assertEqual(file_link_url(request, d), link)


class DownloadSiteCase(TestCase):
    def setUp(self):
        f = open(os.getcwd() + '/media/pier-569314_640.jpg', 'rb')
        UploadFile.objects.create(display_name="test", file=File(f))

    def test_download(self):
        down_file = UploadFile.objects.all().last()

        # Clean uploaded file
        os.remove(down_file.file.path)

        sd = DownloadSite()
        sd.save()
        for down_file in UploadFile.objects.all():
            d = Download(site=sd, down_file=down_file)
            d.save()
        request = Obj()
        request.__dict__['META'] = {}
        request.META['HTTP_HOST'] = 'www.example.com'
        link = '%s%s/%s/site/%s' % (
            'http://',
            request.META.get(
                'HTTP_HOST'),
            presettings.DYNAMIC_LINK_URL_BASE_COMPONENT,
            sd.link_key
        )
        self.assertEqual(site_link_url(request, sd), link)