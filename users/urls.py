from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
	url(r"^$", views.UserListView.as_view(), name="list"),
	url(r"^create/$", views.UserCreationView.as_view(), name="create"),
	url(r"^edit/(?P<pk>\d+)/$", views.UserChangeView.as_view(), name="update"),
	url(r"^(?P<pk>\d+)/$", views.UserDetailView.as_view(), name="detail"),
)