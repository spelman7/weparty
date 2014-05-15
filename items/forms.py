from django import forms
from .models import Item

class ItemForm(forms.ModelForm):

	class Meta:
		model = Item
		exclude = ('owner', 'slug', 'published')

class ImageForm(forms.Form):
	docfile = forms.FileField(
		label='Select a file'
	)
