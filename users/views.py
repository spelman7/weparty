from django.contrib import messages, auth
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormView

from .models import User
from .forms import UserCreationForm, UserChangeForm

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

class UserChangeView(UserActionMixin, UpdateView):
	model = User
	action = 'updated'
	form_class = UserChangeForm

class UserListView(PublishedUserMixin, ListView):
	model = User

class UserDetailView(PublishedUserMixin, DetailView):
	model = User