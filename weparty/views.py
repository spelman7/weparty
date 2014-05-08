from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from items.models import Item
from users.models import User

from wepay import WePay

class HomepageView(TemplateView):
	template_name = "index.html"

# @login_required(login_url='/users/login')
class DashboardView(TemplateView):
	template_name = "dashboard.html"

	def get(self, request, *args, **kwargs):
		uid = request.user.id
		item_list = Item.objects.filter(owner=uid)
		return render(request, self.template_name, {'item_list': item_list})

	def post(self, request, *args, **kwargs):
		access_token = 'STAGE_25361b68e606cc342a7e4ec982fac2139f9f72dd42156237da9468c832f56dce'
		production = False
		client_id = 167754
		client_secret = "da07303f7e"
		email = self.request.user.email
		first_name = self.request.user.name
		last_name = "WeParty"
		wepay = WePay(production, access_token)
		response = wepay.call('/user/register', {
			"client_id":client_id,
			"client_secret":client_secret,
			"email":email,
			"scope":"manage_accounts,view_balance,collect_payments,view_user",
			"first_name":first_name,
			"last_name":last_name,
			"original_ip":"74.125.224.84",
			"original_device":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.102 Safari/534.13"
		})
		print type(response)
		print response
		user_access_token = response[u'access_token']
		wepay2 = WePay(production, user_access_token)
		response2 = wepay.call('/account/create', {
			"name": first_name + " WeParty",
			"description": "WeParty account"
		})
		print response2
		user = User.objects.get(id=request.user.id)
		user.wepayUserId = response[u'user_id']
		user.wepayAccountId = response2[u'account_id']
		user.wepayAccessToken = response[u'access_token']
		user.save()
		return HttpResponseRedirect('/dashboard/')
