from django.conf.urls import url

from . import views

app_name = 'OneTimeLink'

urlpatterns = [
    url(r'^site/([\w-]*)/$', views.site, name='site'),
    url(r'^link/(\w{1,100})$', views.fetch, name='fetch'),
    url(r'^downloadsite/$', views.downloadsite, name='downloadsite'),
]
