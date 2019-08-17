from django.conf.urls import url
from django.urls import path, include

from django.contrib import admin

import picturehunt.views

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path("", picturehunt.views.index, name="index"),
    path("login/", picturehunt.views.login, name="login"),
    path("logout/", picturehunt.views.logout, name="logout"),
]
