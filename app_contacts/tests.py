from django.test import TestCase, Client

# Create your tests here.
class UsersViewTestCase(TestCase):

    def setUp(self):

        #Create the client object
        self.client = Client()


    def test_contactpage_is_accessible(self):
        """
        The contact page must not be accessible without authentication          
        """
        response = self.client.get("contacts/index/")
        self.assertEqual(response.status_code, 404)