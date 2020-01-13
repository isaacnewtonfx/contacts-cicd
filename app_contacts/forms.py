from django import forms
from django.forms import ModelForm
from . models import Contact
from django.utils.translation import gettext as _

class ContactForm(ModelForm):
	class Meta:
		model = Contact
		fields = ['firstname','middlename','lastname','email','tel1','tel2']
		#exclude = ['user_id']


	def clean_tel1(self):
		tel1 = self.cleaned_data['tel1']
		if not tel1.isdigit():
			raise forms.ValidationError(_("This field must be numeric"))
		return self.cleaned_data['tel1']


	def clean_tel2(self):
		tel2 = self.cleaned_data['tel2']
		if tel2 is not None:
			if not tel2.isdigit():
				raise forms.ValidationError(_("This field must be numeric %s" % tel2))			
		return self.cleaned_data['tel2']