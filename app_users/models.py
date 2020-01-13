# This model will be used to extend the defualt user model so that additional information 
# can be collected on a particular user. It holds a 1 to 1 relationship with the default user model

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime,os,hashlib,shutil
from os.path import exists
from PIL import Image

def only_filename(instance, filename):
    
    # get the file extension
    file_extension = filename[-4:]

    # generate a unique prefix code
    unique_prefix = hashlib.md5( filename.encode('utf-8','strict') + str(datetime.datetime.now()).encode('utf-8','strict') ).hexdigest()
    filename = "%s%s" % (unique_prefix, file_extension)

    return filename


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	middlename = models.CharField(max_length = 50,null=True,blank=True)
	phone = models.CharField(max_length = 50,null=True,blank=True)
	photo = models.ImageField(upload_to = only_filename, max_length=1000, null=True, blank=True)
	old_photo_filename = 'default.jpg'

	# grab the initial photo filename and store it on this instance
	def __init__(self, *args, **kwargs):
		super(UserProfile,self).__init__(*args, **kwargs)
		self.old_photo_filename = self.photo.name
		self.hasPhotoUpload = False

	# Override the save functionality to handle photo resizing
	def save(self, *args, **kwargs):

		# call the parent save() method
		super(UserProfile, self).save(*args, **kwargs)


		# now handle photo upload,resize it and move it to the media/images userphotos directory
		if self.hasPhotoUpload:
			image = Image.open(self.photo.path)
			resizedImage = image.resize((200, 200), Image.ANTIALIAS)
			resizedImage.save(self.photo.path)
			sourcepath = self.photo.path
			destination_path = os.path.join(settings.BASE_DIR, 'media_contacts') + "/" + self.photo.name
			shutil.move(sourcepath, destination_path)

			# now delete old user photo from the userphotos directory if only its not the default photo
			if self.old_photo_filename != "" and self.old_photo_filename != "default.jpg" and self.old_photo_filename is not None:
				filepath = os.path.join(settings.BASE_DIR, 'media_contacts') + "/" + self.old_photo_filename
				if( exists(filepath) ):
					os.remove(filepath)


	def image_tag(self):
		return u'<img src="/media_contacts/%s" />' % (self.photo.name)
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True





# Create a property to get user profile
# The [0] fetches for the retrieved or created object from a returning tuple of (object,created)
# The "u" infornt of the lambda expression is the python "self" arguement which is the "instance" of the User Model
# being passed automatically to the function
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])