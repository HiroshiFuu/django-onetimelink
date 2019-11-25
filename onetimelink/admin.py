from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.urls import path
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import DownloadSite, Download, UploadFile

from . import presettings
from . import api

import csv


# Register your models here.
class DownSiteAdmin(admin.ModelAdmin):
    change_list_template = "sitedownload_changelist.html"

    def get_queryset(self, request):
        """catch the request object for list pages"""
        self.request = request
        return super(DownSiteAdmin, self).get_queryset(request)

    list_display = ('customer', 'active', 'link', 'timestamp_creation')
    search_fields = ['customer', 'timestamp_creation']
    list_per_page = 50
    fieldsets = (
        (_(u'Link'), {
            'fields': ('customer', 'active')
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('downloadsite/', self.make_downloadsite)
        ]
        return my_urls + urls


    def make_downloadsite(self, request):
        import time
        customer = Customer(name='name_'+str(round(time.time()*1000)), company='company_'+str(round(time.time()*1000)))
        customer.save()
        sd = DownloadSite(customer=customer)
        sd.save()
        for down_file in UploadFile.objects.all():
            d = Download(site=sd, down_file=down_file)
            d.save()
        return HttpResponseRedirect("../")

    def link(self, obj):
        """Generate download url for the site"""
        sitelink = api.site_link_url(self.request, obj)
        sitelink = u'<span style="color: #FF7F00; ">%s:</span> \
        <a target="new" href="%s/">%s/</a><br/>' \
            % (str(_(u'Site')), sitelink, sitelink)

        return mark_safe(sitelink)
    link.allow_tags = True
    link.short_description = _(u'link')


# Register your models here.
class DownLinkAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """catch the request object for list pages"""
        self.request = request
        return super(DownLinkAdmin, self).get_queryset(request)

    list_display = ('site', 'upload_file', 'file', 'active', 'link',
                    'timestamp_creation')
    search_fields = ['site', 'upload_file', 'timestamp_creation', 'link', 'link_key']
    list_per_page = 50
    fieldsets = (
        (_(u'Link'), {
            'fields': ('site', 'down_file', 'active')
        }),
    )

    def upload_file(self, obj):
        link = reverse('admin:%s_%s_change' % (obj.down_file._meta.app_label, obj.down_file._meta.model_name), args=[obj.down_file.id])
        return mark_safe(f'<a href="{link}">{escape(obj.down_file.__str__())}</a>')
    upload_file.allow_tags = True
    upload_file.short_description = _(u'upload_file')


    def file(self, obj):
        """Shows truncated filename on platform independent length."""
        return str(obj.down_file.file.path).split(presettings.DYNAMIC_LINK_MEDIA)[-1]
    file.allow_tags = True
    file.short_description = _(u'file')

    def link(self, obj):
        """Generate download url from link object"""
        filelink = api.file_link_url(self.request, obj)
        filelink = u'<span style="color: #FF7F00; ">%s:</span> \
        <a target="new" href="%s/">%s/</a><br/>' \
            % (str(_(u'File')), filelink, filelink)

        return mark_safe(filelink)
    link.allow_tags = True
    link.short_description = _(u'link')


admin.site.register(DownloadSite, DownSiteAdmin)
admin.site.register(Download, DownLinkAdmin)


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = [
        'display_name',
        'file',
    ]
    fieldsets = (
        (_(u'Upload Files'), {
            'fields': ('file', 'display_name')
        }),
    )