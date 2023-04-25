from django.test import TestCase, Client
from accounts.models import CustomUser
from django.urls import reverse


class AccountsViewsTestCase(TestCase):
    """
    Test cases for accounts views
    """
    def setUp(self) -> None:
        """
        Sets up the test environment by creating test user and company objects and a test client.
        """
        self.user = CustomUser.objects.create_user(
            username="test_user",
            first_name="XXX",
            last_name="XXX",
            email="user@example.com",
            password="test123@",
            role="user"
        )
        self.company = CustomUser.objects.create_user(
            username="test_company",
            first_name="XXX",
            last_name="XXX",
            email="company@example.com",
            password="test123@",
            role="company"
        )
        self.client = Client()

    def test_register_get_view(self):
        """
        Tests the GET request for the register view and asserts that the response code is 200 and the correct template
        is used.
        """
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/register_user.html")

    def test_user_register_post_view(self):
        """
        Tests the POST request for the user register view and asserts that the response code is 200.
        """
        response = self.client.post(reverse("accounts:register"), {
            "username": "test_user2",
            "first_name": "XXX",
            "last_name": "XXX",
            "email": "user2@example.com",
            "password1": "test123@",
        })
        self.assertEqual(response.status_code, 200)

    def test_company_register_post_view(self):
        """
        Tests the POST request for the company register view and asserts that the response code is 200.
        """
        response = self.client.post(reverse("accounts:register"), {
            "username": "test_company2",
            "first_name": "XXX",
            "last_name": "XXX",
            "email": "company2@example.com",
            "password1": "test123@",
        })
        self.assertEqual(response.status_code, 200)

    def test_success_register_view(self):
        """
        Tests the GET request for the success register view and asserts that the response code is 200 and the correct
        template is used.
        """
        response = self.client.get(reverse("accounts:success_register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/register_success.html")

    def test_login_get_view(self):
        """
        Tests the GET request for the login view and asserts that the response code is 200 and the correct template is
        used.
        """
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_user_login_post_view(self):
        """
        Tests the POST request for the user login view with correct credentials and asserts that the response code is
        302.
        """
        response = self.client.post(reverse("accounts:login"), {
            "username": "test_user",
            "password": "test123@",
        })
        self.assertEqual(response.status_code, 302)

    def test_user_login_post_view_wrong_password(self):
        """
        Tests the POST request for the user login view with incorrect credentials and asserts that the response code is
        200.
        """
        response = self.client.post(reverse("accounts:login"), {
            "username": "test_user",
            "password": "test123",
        })
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Tests the GET request for the logout view and asserts that the response code is 302.
        """
        self.client.login(username="test_user", password="test123@")
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)

    def test_change_password_get_view(self):
        """
        Tests the GET request for the change password view and asserts that the response code is 200 and the correct
        template is used.
        """
        response = self.client.get(reverse("accounts:change_password"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/change_password.html")

    def test_change_password_post_view(self):
        """
        Tests the POST request for the change password view with correct credentials and asserts that the response code
        is 302.
        """
        response = self.client.post(reverse("accounts:change_password"), {
            "email": "user@example.com",
            "old_password": "test123@",
            "new_password": "test12345"
        })
        self.assertEqual(response.status_code, 302)

    def test_change_password_post_view_wrong_password(self):
        """
        Tests the POST request for the change password view with incorrect credentials and asserts that the response
        code is 200.
        """
        response = self.client.post(reverse("accounts:change_password"), {
            "email": "user@example.com",
            "old_password": "test",
            "new_password": "test12345"
        })
        self.assertEqual(response.status_code, 200)

    def test_change_password_success_view(self):
        """
        Tests the GET request for the success password change view and asserts that the response code is 200 and the
        correct template is used.
        """
        response = self.client.get(reverse("accounts:success_password_change"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/password_change_success.html")

    def test_logout_user(self):
        """
        Test the GET request for the logout method and assert the response status.
        """
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)

    def test_company_dashboard_authorized_user(self):
        """
        Test the GET request for the company dashboard view and assert the response status.
        """
        self.client.login(username="test_company", password="test123@")
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_company_dashboard_unauthorized_user(self):
        """
        Test the GET request for the company dashboard view and assert the response status.
        """
        self.client.login(username="test_user", password="test123@")
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 302)