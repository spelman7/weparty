from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Item, Image
from .forms import ItemForm, ImageForm

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

	def get(self, request, *args, **kwargs):
		form = ImageForm()
		slug_lookup = self.kwargs.get('slug')
		item = Item.objects.get(slug=slug_lookup)
		images = Image.objects.filter(item=item)
		item_name = item.name
		item_owner = item.owner
		item_description = item.description
		item_updated = item.updated_at
		return render(request, 'items/item_detail.html', {'images': images, 'form': form, 'item_name': item_name, 'item_owner': item_owner, 'item_description': item_description, 'item_updated': item_updated})

	def post(self, request, *args, **kwargs):
		slug_lookup = self.kwargs.get('slug')
		item = Item.objects.get(slug=slug_lookup)
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Image(docfile = request.FILES['docfile'], item = item)
			newdoc.save()
			return HttpResponseRedirect('/dashboard')
