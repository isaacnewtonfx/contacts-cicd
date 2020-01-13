from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.template.defaultfilters import filesizeformat
from django.conf import settings


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 50)
    password = forms.CharField(max_length = 50, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    # Constructor ( Override default constructor )
    def __init__(self, *args, **kwargs):

        # pop out the request object and add it as an instance attribute
        self.request = kwargs.pop('request', None)

        # now call the parent constructor
        super(LoginForm, self).__init__(*args, **kwargs)


    def clean_remember_me(self):
        if not self.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 50,min_length = 6)
    password = forms.CharField(max_length = 50,min_length = 6)
    conf_password = forms.CharField(max_length = 50,min_length = 6)
    firstname = forms.CharField(max_length = 50)
    middlename = forms.CharField(max_length = 50, required = False)
    lastname = forms.CharField(max_length = 50)
    email = forms.EmailField(max_length = 50)
    phone = forms.CharField(max_length = 50, required = False)
    photo = forms.FileField(allow_empty_file = True,required = False)


    # validate unique username
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))


    # validate confirmed password. Always use fields below(later) to validate fields above(earlier)
    def clean_conf_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['conf_password']:            
            raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data['conf_password']


    # validate unique email
    def clean_email(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("The email already exists. Please try another one."))


    # validate the photo field
    def clean_photo(self):
        photo = self.cleaned_data['photo']
        # raise forms.ValidationError(_(photo.content_type.split('/')[1]))
        if hasattr(photo, 'content_type'):           
            content_type = photo.content_type.split('/')[1]
            if content_type in settings.CONTENT_TYPES:
                if photo.size > settings.MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(photo._size)))
            else:
                raise forms.ValidationError(_('File type is not supported'))
            return photo
        return photo


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length = 50, min_length = 6, widget = forms.PasswordInput)
    new_password = forms.CharField(max_length = 50, min_length = 6, widget = forms.PasswordInput)
    conf_password = forms.CharField(max_length = 50, min_length = 6, widget = forms.PasswordInput)    

    # Constructor ( Override default constructor )
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)


    # validate current password.
    def clean_current_password(self):
        user = self.request.user
        current_password = self.cleaned_data['current_password']

        if not user.check_password(current_password):
            raise forms.ValidationError(_("The current password is incorrect."))
        return self.cleaned_data['current_password']   


    # validate confirmed password. Always use fields below(later) to validate fields above(earlier)
    def clean_conf_password(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['conf_password']:            
            raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data['conf_password']


class PersonalDetailsForm(forms.Form):
    firstname = forms.CharField(max_length = 50)
    middlename = forms.CharField(max_length = 50, required = False)
    lastname = forms.CharField(max_length = 50)
    email = forms.EmailField(max_length = 50)
    phone = forms.CharField(max_length = 50, required = False)
    photo = forms.FileField(allow_empty_file = True,required = False)

    # Constructor ( Override default constructor )
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PersonalDetailsForm, self).__init__(*args, **kwargs)


    # validate unique email
    def clean_email(self):
        user = self.request.user

        if User.objects.filter(email__iexact=self.cleaned_data['email']).exists():
            retrieved_user = User.objects.filter(email__iexact=self.cleaned_data['email'])[0]

            if retrieved_user:
                if retrieved_user.id != user.id:
                    # The email belongs to someone other than the logged_in user
                    raise forms.ValidationError(_("The email already exists. Please try another one."))
                return self.cleaned_data['email']
        return self.cleaned_data['email']


    # validate the photo field
    def clean_photo(self):
        photofield = self.cleaned_data['photo']

        if hasattr(photofield, 'content_type'):           
            content_type = photofield.content_type.split('/')[1]
            if content_type in settings.CONTENT_TYPES:
                if photofield.size > settings.MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(photo._size)))
            else:
                raise forms.ValidationError(_('File type is not supported'))
        return photofield