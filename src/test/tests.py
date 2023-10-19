import unittest
import application
from application import fetch_tasks
class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = application.app.test_client()

    def test_login(self):
        ans = self.app.get('/login')
        self.assertEqual(ans.status_code, 200)

    def test_home(self):
        ans = self.app.get('/home')
        self.assertEqual(ans.status_code, 302)

    def test_forgotPassword_get(self):
        ans = self.app.get('/forgotPassword')
        self.assertEqual(ans.status_code, 200)

    def test_forgotPassword_post(self):
        ans = self.app.post('/forgotPassword', data={
            'email': 'test@example.com'  # Add any required form data here
        })
        self.assertEqual(ans.status_code, 200)


    def test_reset_password_get(self):
        # Assuming that you've generated a valid token here
        token = "InNoaXZha2FuZGhhZ2F0bGExOTk5QGdtYWlsLmNvbSI.ZTB9bQ.ppPhhFPKlxifCqVE8Bob72rQ7D4"
        # Simulate a GET request to the resetPassword route with a valid token
        response = self.app.get(f'/resetPassword/{token}')

        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200

        # Add more assertions here to check the response content or other behaviors

    def test_reset_password_post(self):
        # Assuming you've generated a valid token and user email here
        token = "valid_reset_token"
        user_email = "user@example.com"
        # Simulate a POST request to the resetPassword route with a valid token and form data
        response = self.app.post(f'/resetPassword/{token}', data={
            'email': user_email,
            'new_password': 'new_password',  # Provide form data as needed
        })

        self.assertEqual(response.status_code, 302)  # Check if the response status code is 302 (redirect)


    def test_fetch_tasks(self):
        # Call the fetch_tasks function and check if it runs without raising an exception
        try:
            fetch_tasks()
        except Exception as e:
            self.fail(f"fetch_tasks function raised an exception: {str(e)}")


    def test_recommend(self):
        # Set a user session, which can be done using Flask's testing framework
        with self.app as c:
            with c.session_transaction() as session:
                session['user_id'] = 'your_user_id'  # Replace with a valid user ID

        # Send a GET request to the /recommend route
        response = self.app.get('/recommend')

        # Add assertions to check the response, such as the HTTP status code
        self.assertEqual(response.status_code, 200)  # Modify this based on your application's expected behavior


    def test_send_email_reminders(self):
        # Set a user session and add user's email
        with self.app as c:
            with c.session_transaction() as session:
                session['user_id'] = 'your_user_id'  # Replace with a valid user ID
                session['email'] = 'test@example.com'  # Replace with a valid email

        # Send a POST request to the /send_email_reminders route
        response = self.app.post('/send_email_reminders', data={
            'duedate': '2023-10-30'  # Replace with a valid due date
        })

        # Add an assertion to check the HTTP status code
        self.assertEqual(response.status_code, 200) 


    def test_dashboard(self):
        ans = self.app.get('/dashboard')
        self.assertEqual(ans.status_code, 200)

    # Add more test cases for other routes

if __name__ == '__main__':
    unittest.main()
