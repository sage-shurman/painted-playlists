"""
WSGI config for painted_playlists project.

This file contains the WSGI configuration required to serve up your
web application at http://example.com. You can use this file to
configure your WSGI server to load your application.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'painted_playlists' project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "painted_playlists.settings")

# Get the WSGI application for the project
application = get_wsgi_application()
