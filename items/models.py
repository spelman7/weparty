from django.db import models
from users.models import User
from django.template.defaultfilters import slugify

class ItemManager(models.Manager):
	def live(self):
		return self.model.objects.filter(published=True)

class Item(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True, editable=False)
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, blank=True, default='')
	description = models.TextField()
	published = models.BooleanField(default=True)
	owner = models.ForeignKey(User, related_name="items")
	objects = ItemManager()

	class Meta:
		ordering = ["-created_at", "name"]

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super(Item, self).save(*args, **kwargs)

	@models.permalink
	def get_absolute_url(self):
		return ("items:detail", (), {"slug": self.slug})

DEFAULT_ITEM_KEY = 1

class Image(models.Model):
	docfile = models.FileField(upload_to='images/%Y/%m/%d')
	item = models.ForeignKey(Item, related_name="images", default=DEFAULT_ITEM_KEY)
