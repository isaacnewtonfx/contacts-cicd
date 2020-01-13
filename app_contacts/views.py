import datetime
import os

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.template.loader import get_template
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages

from . forms import ContactForm
from . models import Contact

from xhtml2pdf import pisa
from pprint import pprint



class IndexView(View):
	
	def get(self, request):

		# function level authorization
		# if(request.user.has_perm('app_contacts.view_contact') == False):
		# 	referer = request.META['HTTP_REFERER']
		# 	return HttpResponse("<h4>Sorry, you don't have permission to view. <a href=%s>Return</a></h4>" % referer )

		# get all contacts for this user
		contacts = request.user.contact_set.all()
		data = {'contacts':contacts}
		return render(request, 'app_contacts/index.html', data)


class AddView(View):

	def get(self, request):
		# if(request.user.has_perm('app_contacts.add_contact') == False):
		# 	referer = request.META['HTTP_REFERER']
		# 	return HttpResponse("<h4>Sorry, you don't have permission to add. <a href=%s>Return</a></h4>" % referer )

		return render(request, 'app_contacts/add.html')

	def post(self,request):
		# if(request.user.has_perm('app_contacts.add_contact') == False):
		# 	referer = request.META['HTTP_REFERER']
		# 	return HttpResponse("<h4>Sorry, you don't have permission to add. <a href=%s>Return</a></h4>" % referer )


		ContactModel = Contact(user = request.user)
		form = ContactForm(request.POST, instance = ContactModel)

		if form.is_valid():		

			form.save()
			messages.add_message(request, messages.SUCCESS, "Contact added successfully.You may add more")
			return HttpResponseRedirect('/contacts/add')

		else:
			return render(request, 'app_contacts/add.html', {'contactform': form})


class EditView(View):
	def get(self, request, pk):

		# get the contact object from the database
		ContactModel = Contact.objects.get(pk = pk)

		# bind it to a Contact Form
		form = ContactForm(instance = ContactModel)
		

		# prepare data
		data = {'contactform':form, 'ContactID':pk}

		return render(request, 'app_contacts/edit.html',data)	

	def post(self, request, pk):
		ContactModel = Contact.objects.get(pk = pk)
		form = ContactForm(request.POST, instance = ContactModel)

		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Contact updated successfully")
			return HttpResponseRedirect('/contacts/index')
		else:
			return render(request, 'app_contacts/edit.html', {'contactform': form, 'ContactID':pk})


class DeleteView(View):
	def get(self, request, pk):

		#get the contact from the database
		ContactModel = Contact.objects.get(pk = pk)

		#create a dialog
		data = {
			'dialog_title' : "Confirm Delete",
			'dialog_msg' : "Do you want to permanently delete %s?" % ContactModel,
			'action_url' : "contacts:delete",
			'args' : pk
		}
		
		#show dialog
		return render(request, 'layout/dialog.html', data)

	def post(self, request, pk):

		if request.POST['option'] == "no":
			messages.add_message(request, messages.SUCCESS, "Action was cancelled")
			return HttpResponseRedirect('/contacts/index')
		else:

			#get the contact from the database
			ContactModel = Contact.objects.get(pk = pk)

			#get contact name
			name = ContactModel.__str__()

			#delete the contact
			ContactModel.delete()

			#put a success message in the session
			messages.add_message(request, messages.SUCCESS, "%s was deleted successfully" % name)

			#redirect to the index page
			return HttpResponseRedirect('/contacts/index')


def ReportView(request):

	today = datetime.datetime.today()
	contacts = request.user.contact_set.all()

	#request.scheme               # http or https
    #request.META['HTTP_HOST']    # example.com
    #request.path                 # /some/content/1/
	domain = request.scheme + "://" + request.META['HTTP_HOST']

	data = {'today':today, 'contacts':contacts, 'domain' : domain}

	template = get_template('app_contacts/rptAllContacts.html')
	html  = template.render(data)

	file = default_storage.open(os.path.join(settings.MEDIA_ROOT, 'report.pdf'), 'w+b')
	pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,encoding='utf-8')

	file.seek(0)
	pdf = file.read()
	file.close() 
	os.unlink(file.name)
	           
	return HttpResponse(pdf, 'application/pdf')
	response['Content-Disposition'] = 'attachment; filename=report.pdf'