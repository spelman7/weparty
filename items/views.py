from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Item
from .forms import ItemForm

class PublishedItemMixin(object):
	def get_queryset(self):
		return self.model.objects.live()
		
class ItemActionMixin(object):
	def form_valid(self, form):
		msg = 'Item {0}!'.format(self.action)
		messages.info(self.request, msg)
		return super(ItemActionMixin, self).form_valid(form)
		
class ItemCreateView(ItemActionMixin, CreateView):
	model = Item
	action = 'created'
	form_class = ItemForm
	
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(ItemCreateView, self).form_valid(form)

class ItemUpdateView(ItemActionMixin, UpdateView):
	model = Item
	action = 'updated'
	form_class = ItemForm

class ItemListView(PublishedItemMixin, ListView):
	model = Item

class ItemDetailView(PublishedItemMixin, DetailView):
	model = Item
