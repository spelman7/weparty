from django.contrib import messages, auth
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView
from django.views.generic.edit import FormView
from wepay import WePay

from .models import User
from .forms import UserCreationForm, UserChangeForm, UserLoginForm

import json

class PublishedUserMixin(object):
	def get_queryset(self):
		return self.model.objects.active()

class UserActionMixin(object):
	def form_valid(self, form):
		msg = 'User {0}!'.format(self.action)
		messages.info(self.request, msg)
		return super(UserActionMixin, self).form_valid(form)

class UserCreationView(UserActionMixin, CreateView):
	model = User
	action = 'created'
	form_class = UserCreationForm

	def form_valid(self, form):
		# do things
		return super(UserCreationView, self).form_valid(form)

class RegisterView(FormView):
	template_name = "register.html"
	form_class = UserCreationForm
	model = User
	success_url = "/dashboard/"

	def form_valid(self, form):
		form.save()
		new_user = authenticate(username=self.request.POST['email'],password=self.request.POST['password1'])
		login(self.request, new_user)
		return HttpResponseRedirect(self.get_success_url())

class LoginView(FormView):
	template_name = "login.html"
	form_class = UserLoginForm
	model = User
	success_url = "/dashboard/"

	def form_valid(self, form):
		login_user = authenticate(username=self.request.POST['email'],password=self.request.POST['password'])
		if login_user is not None:
			if login_user.is_active:
				login(self.request, login_user)
				return HttpResponseRedirect(self.get_success_url())
			else:
				return HttpResponse("Your WeParty account is disabled")
		else:
			return HttpResponse("Invalid login details supplied")

class LogoutView(RedirectView):
	permanent = False
	query_string = True
	pattern_name = 'home'

	def get_redirect_url(self, *args, **kwargs):
		if self.request.user.is_authenticated():
			logout(self.request)
		return super(LogoutView, self).get_redirect_url(*args, **kwargs)

class UserChangeView(UserActionMixin, UpdateView):
	model = User
	action = 'updated'
	form_class = UserChangeForm

class UserListView(PublishedUserMixin, ListView):
	model = User

class UserDetailView(PublishedUserMixin, DetailView):
	model = User
