from accounts.models import CustomUser
from django.test import TestCase


class TestUserModel(TestCase):
    """
    Test if CustomUser object is created correctly.
    """
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            first_name="Kacper",
            last_name="Kowalski",
            username="test",
            email="user@example.com",
            password="test123@",
            role="user"
        )
        self.company = CustomUser.objects.create(
            username="company",
            email="company@example.com",
            password="test123@",
            role="company"
        )

    def test_user_creation(self) -> None:
        """
        Test if user is created correctly.
        """
        self.assertEqual(self.user.first_name, "Kacper")
        self.assertEqual(self.user.last_name, "Kowalski")
        self.assertEqual(self.user.username, "test")
        self.assertEqual(self.user.email, "user@example.com")
        self.assertEqual(self.user.role, "user")

    def test_company_user_creation(self) -> None:
        """
        Test if company user is created correctly.
        """
        self.assertEqual(self.company.username, "company")
        self.assertEqual(self.company.email, "company@example.com")
        self.assertEqual(self.company.role, "company")
