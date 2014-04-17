from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from items.models import Item

class HomepageView(TemplateView):
	template_name = "index.html"
	
class DashboardView(TemplateView):
	template_name = "dashboard.html"
	
	def get(self, request, *args, **kwargs):
		uid = request.user.id
		item_list = Item.objects.filter(owner=uid)
		return render(request, self.template_name, {'item_list': item_list})