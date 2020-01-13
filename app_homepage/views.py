from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.http import HttpResponse

class IndexView(View):
	def get(self, request):
		return render(request, 'app_homepage/index.html')

class AboutView(View):
	def get(self, request):
  		return render(request, 'app_homepage/about.html')

class ContactView(View):
	def get(self, request):
  		return render(request, 'app_homepage/contact.html')


def showError404(request):
	return HttpResponse ("error 400 occured")
    #return render(request, 'layout/error404.html', status = 404)

def showError500(request):
	return HttpResponse ("error 500 occured")
	#return render(request, 'layout/error500.html', status = 500)