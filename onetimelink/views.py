from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str

from .models import DownloadSite, Download, IsExpiredError, UploadFile
from . import presettings

import os

# Create your views here.
def downloadsite(request):
    if request.method == 'POST':
        sd = DownloadSite()
        sd.save()
        for down_file in UploadFile.objects.all():
            d = Download(site=sd, down_file=down_file)
            d.save()
        return HttpResponseRedirect('../site/' + sd.link_key +'/')
    return HttpResponse('Method Not Allowed', status=405)


def expired(key):
    expired_objects = Download.objects.filter(active=False)
    # check expired objects
    for obj in expired_objects:
        if key == obj.link_key:
            return obj


def active(key):
    active_objects = Download.objects.filter(active=True)
    # check active objects
    for obj in active_objects:
        if key == obj.link_key:
            return obj


def error(request, text=_(u'Sorry, your request is not available')):
    """returns the error page"""
    extra_context = {'message': text}
    template = 'not_avallible.html'
    return render(request, template, extra_context)


def site(request, offset):
    """process site requests"""
    obj = {'actives': [], 'expired': [], 'not_exist': []}

    sd = DownloadSite.objects.all().filter(link_key=offset).first()
    if sd is None:
        extra_context = {'message': 'This site does not exist'}
        template = 'not_avallible.html'
        return render(request, template, extra_context)

    # Test if keys are valid
    for download in Download.objects.all().filter(site=sd):
        key = download.link_key
        if active(key):
            obj['actives'].append(active(key))
        elif expired(key):
            obj['expired'].append(expired(key))
        else:
            obj['not_exist'].append(key)

    template = 'site.html'
    extra_context = {
        'basepath': presettings.DYNAMIC_LINK_URL_BASE_COMPONENT,
        'downloads': obj
    }
    return render(request, template, extra_context)


def fetch(request, offset):
    """process link requests. make desissions for every single download link"""
    if active(offset):
        return provide(request, offset)
    elif expired(offset):
        return error(request, presettings.TEXT_REQUEST_IS_EXPIRED)
    else:
        return error(request, presettings.TEXT_REQUEST_DOES_NOT_EXIST)


@cache_control(private=True)
def provide(request, key):
    """
    Return a download without the rael path to the served file.
    The content will served by a stream.

    The file will read in byte code to a socket wich will be
    used in the response object. Headers in the response will
    set for the specific served content referable to its type.
    """
    stored_file_obj = Download.objects.get(link_key=key)
    try:
        # we use a model method to validate and deliver the path
        filepath = stored_file_obj.get_path()
    except IsExpiredError as e:
        return error(request, e.value)

    # make file path suitable for different installations
    delimiter = presettings.DYNAMIC_LINK_MEDIA.strip('/').strip('\\').split('/')[-1]
    # now we use the objects get_path() method to be sure
    # the object instance keep up to date.
    file_path = os.path.normpath(
        presettings.DYNAMIC_LINK_MEDIA + filepath.split(delimiter)[-1]
    )

    # get file parameters
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as fr:
                response = HttpResponse(
                    fr.read(), content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename=%s' \
                    % smart_str(file_name)
                response['X-Sendfile'] = smart_str(file_path)
                # response['X-Accel-Redirect'] = smart_str(file_path) # For ngnix
                response['Content-Length'] = file_size

                return response
        except IOError:
            stored_file_obj.active = False
            stored_file_obj.save()  # only raise the following once
            return HttpResponseNotFound(unicode(_(u'File not found!')))  # admin

    extra_context = {'message': 'Something went wrong...'}
    template = 'not_avallible.html'
    return render(request, template, extra_context)
