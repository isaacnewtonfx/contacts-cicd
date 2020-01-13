from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE) # required
	firstname = models.CharField(max_length = 50) # required
	middlename = models.CharField(max_length = 50, blank=True, null=True)
	lastname = models.CharField(max_length = 50) # required
	email = models.EmailField(max_length = 50) # required
	tel1 = models.CharField(max_length = 50) # required
	tel2 = models.CharField(max_length = 50, blank=True, null=True)

	def __str__(self):
		return '%s %s %s' % (self.firstname, self.middlename, self.lastname)