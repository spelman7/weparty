from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

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

class UserChangeView(UserActionMixin, UpdateView):
	model = User
	action = 'updated'
	form_class = UserChangeForm

class UserListView(PublishedUserMixin, ListView):
	model = User

class UserDetailView(PublishedUserMixin, DetailView):
	model = User