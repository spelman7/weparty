from django.contrib import admin

from .models import Item

class ItemAdmin(admin.ModelAdmin):
	date_heirarchy = "created_at"
	fields = ("published", "name", "slug", "description", "owner")
	list_display = ["published", "name", "updated_at"]
	list_display_links = ["name"]
	list_editable = ["published"]
	list_filter = ["published", "updated_at", "owner"]
	prepopulated_fields = {"slug": ("name",)}
	search_field = ["name", "description"]
	
admin.site.register(Item, ItemAdmin)