from django.urls import re_path

from . import views

app_name = 'OneTimeLink'

urlpatterns = [
    re_path('site/([\w-]*)/$', views.site, name='site'),
    re_path('link/(\w{31})/.*', views.fetch, name='fetch'),
    re_path('downloadsite/$', views.downloadsite, name='downloadsite'),
]
