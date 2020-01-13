from django.test import TestCase, Client

# Create your tests here.
class HomepageViewTestCase(TestCase):

    def setUp(self):

        #Create the client object
        self.client = Client()

    
    def test_homepage_is_accessible(self):
        """
        The homepage must be accessible without any authentication          
        """
        response = self.client.get("/contacts/")
        self.assertEqual(response.status_code, 200)


    def test_aboutpage_is_accessible(self):
        """
        The about us page must be accessible without any authentication          
        """
        response = self.client.get("/contacts/about/")
        self.assertEqual(response.status_code, 200)


    def test_contactuspage_is_accessible(self):
        """
        The contact us page must be accessible without any authentication          
        """
        response = self.client.get("/contacts/contact/")
        self.assertEqual(response.status_code, 200)