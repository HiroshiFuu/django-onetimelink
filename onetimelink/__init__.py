import version
import os
import django
import sys

__author__ = "FENG Hao"
__copyright__ = "Copyright (c) " + "25.11.2019" + " FENG Hao"
__licence__ = """BSD-3-Clause Licence"""


def CKINST():
    """function to find problems of the installation."""
    print('I will try to find errors for you!')

    djv = django.VERSION[:2]

    def strform(val):
        """returns formated version tuples"""
        return str(val).strip('()').replace(' ', '').replace(',', '.')

    # Errors
    dja = django.VERSION[:2]
    pyver = sys.version_info[:2]
    error = True
    if not dja >= (2, 0):
        print('')
        print('Hint! Django requires 2.0 or greater which currently is' % dja)
    else:
        error = False
    if not pyver >= (3, 4):
        print('')
        print('Hint! Python requires 3.4 or greater which currently is' % pyver)
    else:
        error = False

    # success message
    if not error:
        print("No errors!")
