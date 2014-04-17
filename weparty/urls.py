from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r"^$", views.HomepageView.as_view(), name="home"),
	url(r"^items/", include("items.urls", namespace="items")),
	url(r"^users/", include("users.urls", namespace="users")),
    url(r'^admin/', include(admin.site.urls)),
)