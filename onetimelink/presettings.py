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
# /www.example.com/DYNAMIC_LINK_URL_BASE_COMPONENT/link/3839hd8HKl3/example.zip
DYNAMIC_LINK_URL_BASE_COMPONENT = getattr(
    settings,
    'DYNAMIC_LINK_URL_BASE_COMPONENT',
    'OneTimeLink'
)

# It's here because of not violate the DRY priciple.
TEXT_REQUEST_DOES_NOT_EXIST = _(u'This request does not exist.')
TEXT_REQUEST_IS_EXPIRED = _(u'Sorry, this request is already expired')
