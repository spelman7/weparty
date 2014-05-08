from django.conf.urls import patterns, url

from . import views
from .forms import UserCreationForm, UserLoginForm

urlpatterns = patterns('',
	url(r"^$", views.UserListView.as_view(), name="list"),
	url(r"^register/$", views.RegisterView.as_view(form_class=UserCreationForm, success_url="/dashboard/"), name="register"),
	url(r"^login/$", views.LoginView.as_view(form_class=UserLoginForm, success_url="/dashboard/"), name="login"),
	url(r"^logout/$", views.LogoutView.as_view(), name="logout"),
	url(r"^edit/(?P<pk>\d+)/$", views.UserChangeView.as_view(), name="update"),
	url(r"^(?P<pk>\d+)/$", views.UserDetailView.as_view(), name="detail"),
)
