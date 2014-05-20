from django.contrib import admin

from .models import Item, Image

class ItemAdmin(admin.ModelAdmin):
	date_heirarchy = "created_at"
	fields = ("published", "name", "slug", "description", "owner")
	list_display = ["published", "name", "updated_at"]
	list_display_links = ["name"]
	list_editable = ["published"]
	list_filter = ["published", "updated_at", "owner"]
	prepopulated_fields = {"slug": ("name",)}
	search_field = ["name", "description"]

class ImageAdmin(admin.ModelAdmin):
	fields = ("docfile", "item")

admin.site.register(Item, ItemAdmin)

admin.site.register(Image, ImageAdmin)
