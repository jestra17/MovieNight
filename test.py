from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

	#Ensure that flask was set up correctly
	def test_index(self):
		tester = app.test_client(self)
		response = tester.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 200)

	#Ensure that loggin loads
	def test_login_page_loads(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type='html/text')
		self.assertTrue('Please sign in' in response.data)

	#Ensure that the login behaves given incorrect credentials
	def test_login_incorrect_login(self):
		tester = app.test_client(self)
		response = tester.post('/login', 
			data=dict(username="joezanini", password="12345678"),
			follow_redirects=True)
		self.assertIn('Invalid username or password' in response.data)



if __name__ == '__main__':
	unittest.main()