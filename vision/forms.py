from django import forms
from .models import UploadedImage


class ImageUploadForm(forms.ModelForm):
	class Meta:
		model = UploadedImage
		fields = ['image']