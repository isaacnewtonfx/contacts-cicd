from django.contrib import admin
from .models import Contact
from django.contrib.auth.models import Permission


class ContactAdmin(admin.ModelAdmin):
	list_display = ('firstname','middlename','lastname','email','tel1','tel2')
	search_fields = ('firstname','middlename','lastname','email','tel1','tel2')
	# list_filter = ('firstname','lastname')

admin.site.register(Contact,ContactAdmin)
admin.site.register(Permission)