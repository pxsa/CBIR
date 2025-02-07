from django.contrib import admin
from .models import UploadedImage


# Register your models here.
class UploadedImageAdmin(admin.ModelAdmin):
	list_display = ('id', 'image', 'uploaded_at')
	search_fields = ('image', )
	list_filter = ('uploaded_at', )

admin.site.register(UploadedImage, UploadedImageAdmin)
