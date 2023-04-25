from django.test import TestCase, Client
from accounts.models import CustomUser
from django.urls import reverse
from offers.models import (
    Level,
    Position,
    Country,
    Localization,
    Contract,
    Requirements,
    Offer,
    Application
)


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

        self.name = "Junior Python Developer"
        self.position = Position.objects.create(
            position_name="Python"
        )
        self.level = Level.objects.create(
            level_name="Junior"
        )
        self.contract = Contract.objects.create(
            contract_type="B2B"
        )
        self.requirements = Requirements.objects.create(
            name="Git"
        )
        self.country = Country.objects.create(
            name="Poland"
        )
        self.localization = Localization.objects.create(
            country=self.country,
            city="Warsaw"
        )
        self.description = "Junior Python Developer with 10 years exp"
        self.salary_from = 20000
        self.salary_to = 25000
        self.remote = True
        self.custom_user = CustomUser.objects.create(
            role='company',
            username='Nokia',
            email="nokia123@wp.pl",
            password="XXXXXXX"
        )
        self.company = self.custom_user
        self.offer = Offer.objects.create(
            name=self.name,
            position=self.position,
            level=self.level,
            description=self.description,
            localization=self.localization,
            salary_from=self.salary_from,
            salary_to=self.salary_to,
            remote=self.remote,
            company=self.company,
            address="Zielona 4"
        )
        self.offer.contract.add(self.contract)
        self.offer.requirements.add(self.requirements)

    # def test_register_get_view(self):
    #     """
    #     Tests the GET request for the register view and asserts that the response code is 200 and the correct template
    #     is used.
    #     """
    #     response = self.client.get(reverse("accounts:register"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "auth/register_user.html")
    #
    # def test_user_register_post_view(self):
    #     """
    #     Tests the POST request for the user register view and asserts that the response code is 200.
    #     """
    #     response = self.client.post(reverse("accounts:register"), {
    #         "username": "test_user2",
    #         "first_name": "XXX",
    #         "last_name": "XXX",
    #         "email": "user2@example.com",
    #         "password1": "test123@",
    #     })
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_company_register_post_view(self):
    #     """
    #     Tests the POST request for the company register view and asserts that the response code is 200.
    #     """
    #     response = self.client.post(reverse("accounts:register"), {
    #         "username": "test_company2",
    #         "first_name": "XXX",
    #         "last_name": "XXX",
    #         "email": "company2@example.com",
    #         "password1": "test123@",
    #     })
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_success_register_view(self):
    #     """
    #     Tests the GET request for the success register view and asserts that the response code is 200 and the correct
    #     template is used.
    #     """
    #     response = self.client.get(reverse("accounts:success_register"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "auth/register_success.html")
    #
    # def test_login_get_view(self):
    #     """
    #     Tests the GET request for the login view and asserts that the response code is 200 and the correct template is
    #     used.
    #     """
    #     response = self.client.get(reverse("accounts:login"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "auth/login.html")
    #
    # def test_user_login_post_view(self):
    #     """
    #     Tests the POST request for the user login view with correct credentials and asserts that the response code is
    #     302.
    #     """
    #     response = self.client.post(reverse("accounts:login"), {
    #         "username": "test_user",
    #         "password": "test123@",
    #     })
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_user_login_post_view_wrong_password(self):
    #     """
    #     Tests the POST request for the user login view with incorrect credentials and asserts that the response code is
    #     200.
    #     """
    #     response = self.client.post(reverse("accounts:login"), {
    #         "username": "test_user",
    #         "password": "test123",
    #     })
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_logout_view(self):
    #     """
    #     Tests the GET request for the logout view and asserts that the response code is 302.
    #     """
    #     self.client.login(username="test_user", password="test123@")
    #     response = self.client.get(reverse("accounts:logout"))
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_change_password_get_view(self):
    #     """
    #     Tests the GET request for the change password view and asserts that the response code is 200 and the correct
    #     template is used.
    #     """
    #     response = self.client.get(reverse("accounts:change_password"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "auth/change_password.html")
    #
    # def test_change_password_post_view(self):
    #     """
    #     Tests the POST request for the change password view with correct credentials and asserts that the response code
    #     is 302.
    #     """
    #     response = self.client.post(reverse("accounts:change_password"), {
    #         "email": "user@example.com",
    #         "old_password": "test123@",
    #         "new_password": "test12345"
    #     })
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_change_password_post_view_wrong_password(self):
    #     """
    #     Tests the POST request for the change password view with incorrect credentials and asserts that the response
    #     code is 200.
    #     """
    #     response = self.client.post(reverse("accounts:change_password"), {
    #         "email": "user@example.com",
    #         "old_password": "test",
    #         "new_password": "test12345"
    #     })
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_change_password_success_view(self):
    #     """
    #     Tests the GET request for the success password change view and asserts that the response code is 200 and the
    #     correct template is used.
    #     """
    #     response = self.client.get(reverse("accounts:success_password_change"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "auth/password_change_success.html")
    #
    # def test_logout_user(self):
    #     """
    #     Test the GET request for the logout method and assert the response status.
    #     """
    #     response = self.client.get(reverse("accounts:logout"))
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_company_dashboard_authorized_user(self):
    #     """
    #     Test the GET request for the company dashboard view and assert the response status.
    #     """
    #     self.client.login(username="test_company", password="test123@")
    #     response = self.client.get(reverse("accounts:dashboard"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "profile/company_dashboard.html")
    #
    # def test_company_dashboard_unauthorized_user(self):
    #     """
    #     Test the GET request for the company dashboard view and assert the response status.
    #     """
    #     self.client.login(username="test_user", password="test123@")
    #     response = self.client.get(reverse("accounts:dashboard"))
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_user_profile_authorized_user(self):
    #     """
    #     Test the GET request for the user profile view and assert the response status.
    #     """
    #     self.client.login(username="test_user", password="test123@")
    #     response = self.client.get(reverse("accounts:user_profile"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "profile/user_profile.html")
    #
    # def test_user_profile_unauthorized_user(self):
    #     """
    #     Test the GET request for the user profile view and assert the response status.
    #     """
    #     self.client.login(username="test_company", password="test123@")
    #     response = self.client.get(reverse("accounts:user_profile"))
    #     self.assertEqual(response.status_code, 302)

    def test_offer_create_view_authorized_user_get(self):
        """
        Test for GET request for the offer create view using client log in with role 'company'
        """

        self.client.login(username="test_company", password="test123@")
        response = self.client.get(reverse("accounts:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "offer_create.html")

    def test_offer_create_view_unauthorized_user_get(self):
        """
        Test for GET request for the offer create view using client log in with role 'user'
        """

        self.client.login(username="test_user", password="test123@")
        response = self.client.get(reverse("accounts:create"))
        self.assertEqual(response.status_code, 403)
