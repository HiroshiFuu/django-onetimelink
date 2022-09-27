from django.conf import settings
from django.utils.translation import ugettext_lazy as _


KEY_POLL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
KEY_LENGTH = 31

# A path to a directory from witch walk down so you can choose your files.
DYNAMIC_LINK_MEDIA = getattr(
    settings,
    'DYNAMIC_LINK_MEDIA',
    settings.MEDIA_ROOT
)

# A string that modify the serve url path:
# www.example.com/DYNAMIC_LINK_URL_BASE_COMPONENT/link/3839hd8HKl3/example.zip
DYNAMIC_LINK_URL_BASE_COMPONENT = getattr(
    settings,
    'DYNAMIC_LINK_URL_BASE_COMPONENT',
    'OneTimeLink'
)

# Prefixes if FORCE_SCRIPT_NAME
DYNAMIC_LINK_URL = ''
DYNAMIC_LINK_USE_FORCE_SCRIPT_NAME = getattr(
    settings,
    'DYNAMIC_LINK_USE_FORCE_SCRIPT_NAME',
    False
)
if DYNAMIC_LINK_USE_FORCE_SCRIPT_NAME and settings.FORCE_SCRIPT_NAME:
    DYNAMIC_LINK_URL = settings.FORCE_SCRIPT_NAME + '/' + DYNAMIC_LINK_URL_BASE_COMPONENT
else:
    DYNAMIC_LINK_URL = '/' + DYNAMIC_LINK_URL_BASE_COMPONENT
DYNAMIC_LINK_URL = DYNAMIC_LINK_URL.replace('//', '/')

# Uploaded files base directory
DYNAMIC_LINK_UPLOAD_TO = getattr(
    settings,
    'DYNAMIC_LINK_UPLOAD_TO',
    ''
)

# Setting for schema protocol
DYNAMIC_LINK_SCHEMA_PROTO = getattr(
    settings,
    'DYNAMIC_LINK_SCHEMA_PROTO',
    'http'
)

# Setting for HTTP Host override
DYNAMIC_LINK_HTTP_HOST = getattr(
    settings,
    'DYNAMIC_LINK_HTTP_HOST',
    None
)

# It's here because of not violate the DRY priciple.
TEXT_REQUEST_DOES_NOT_EXIST = _(u'This request does not exist.')
TEXT_REQUEST_IS_EXPIRED = _(u'Sorry, this request is already expired')
