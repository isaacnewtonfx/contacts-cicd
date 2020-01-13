from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'contacts'
urlpatterns = [
	path('index/', login_required( views.IndexView.as_view() ), name='index'),
	path('add/', login_required( views.AddView.as_view() ), name='add'),
	path('edit/<int:pk>', login_required(views.EditView.as_view() ), name='edit'),
	path('delete/<int:pk>', login_required(views.DeleteView.as_view() ), name='delete'),
	path('report/', login_required( views.ReportView ), name='report'),
]