"""
A module serving custom context processors for Django.
"""
from django.conf import settings

def app_info(request):
    """
    Fetches information about the application, such as:

    * ``APP_NAME`` the application name (as defined in settings.py)
    * ``APP_VERSION`` the version of the application (as defined in version.txt)

    :returns: a dict of global information about the application
    """
    return {
        'APP_NAME': settings.APP_NAME,
        'APP_VERSION': settings.APP_VERSION,
    }