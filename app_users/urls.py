from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'users'
urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('registration/', views.RegistrationView.as_view(), name='registration'),
	path('manage/', login_required( views.ManageView.as_view() ), name='manage'),
	path('manage_personal_details/', login_required( views.ManagePersonalDetailsView.as_view() ), name='manage_personal_details'),
	path('change_user_password/', login_required( views.ChangeUserPasswordView.as_view() ), name='change_user_password'),
]