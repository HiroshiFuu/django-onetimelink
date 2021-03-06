===========
Description
===========

A Django file streaming application to provide download links that only valid for one time click. Ispired by django-dynamic-link

**License**

    BSD-3-Clause license

**Notes**

    * Tested with Django 2.2

========
Features
========

    * One-time only download ink 

============
Installation
============

**Dependences**

    * This app only

**Installation**

    *Installation with pip (recommended)*

        *Pip will download and install the package and take care of all the dependences.
        If you havn't pip on your system then install setuptools first after that run "easy_install pip".
        After that you can use pip in your terminal window.*

        * Use the stable release (recommended)::

                pip install django-onetimelink

        * With pip you can also uninstall::

            pip uninstall django-onetimelink

**test your installation**

    Go to console and type::

        python

    ... then type::
    
        >>> import onetimelink
        >>> onetimelink.CKINST()
        >>> help(onetimelink)
        >>> exit()
    
=====
Setup
=====
    
    * Add "onetimelink" to you installed apps in the settings file.
    * Make sure that:

        1.  Your Admin is enabled ('django.contrib.admin', is in your INSTALLED_APPS).
        2.  'django.contrib.auth.context_processors.auth', (also for admin) is in TEMPLATE_CONTEXT_PROCESSORS.
        3.  'django.core.context_processors.request', is in TEMPLATE_CONTEXT_PROCESSORS.

    * Add the following to your urls.py:

        1.  from django.conf.urls import include, url
        2.  from onetimelink import presettings
        3.  url(r'%s/' % presettings.DYNAMIC_LINK_URL_BASE_COMPONENT, include('onetimelink.urls')),
        
    * Finally run::
    
        python manage.py migrate
        python manage.py runserver

**Make it custom**

    Use the global settings.py in your projects root to overwrite the applications presettings with the following variables.

    DYNAMIC_LINK_MEDIA

        - Default: settings.MEDIA_ROOT
        - A path to a directory. From this point you can walk down the subdirectories to choose your files to serve.

    DYNAMIC_LINK_URL_BASE_COMPONENT
    
        - Default: 'OneTimeLink'
        - A string that modifies your url serve path.
        - Example: www.example.com/DYNAMIC_LINK_URL_BASE_COMPONENT/link/3839hd8HKl3/example.zip.

=====
Usage
=====

Open the admin interface and go to "OneTimeLink" section. The rest should be self-explanatory.

**Hints**

    * Upload Files to upload the file to DYNAMIC_LINK_MEDIA
    * The filename from the in Upload Files is only for human readability. You can delete or change these filenames in any way you want.
    * Trough the action button you can serve a site with all the files from Upload Files.