from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
	url(r"^$", views.ItemListView.as_view(), name="list"),
	url(r"^create/$", views.ItemCreateView.as_view(), name="create"),
	url(r"^edit/(?P<slug>[\w-]+)/$", views.ItemUpdateView.as_view(), name="update"),
	url(r"^(?P<slug>[\w-]+)/$", views.ItemDetailView.as_view(), name="detail"),
)