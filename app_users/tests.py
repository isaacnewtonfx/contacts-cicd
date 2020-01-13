from django.test import TestCase, Client

# Create your tests here.
class UsersViewTestCase(TestCase):

    def setUp(self):

        #Create the client object
        self.client = Client()


    def test_loginpage_is_accessible(self):
        """
        The login page must be accessible without any authentication          
        """
        response = self.client.get("/contacts/users/login/")
        self.assertEqual(response.status_code, 200)


    def test_registrationpage_is_accessible(self):
        """
        The registration page must be accessible without any authentication          
        """
        response = self.client.get("/contacts/users/registration/")
        self.assertEqual(response.status_code, 200)