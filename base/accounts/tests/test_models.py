from accounts.models import CustomUser, CompanyReview
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


class CompanyReviewTestCase(TestCase):
    def setUp(self) -> None:
        self.company = CustomUser.objects.create(
            username="CompanyX",
            email="company@example.com",
            password="Test123@",
            role="company"
        )
        self.company_review = CompanyReview.objects.create(
            choose_rate=5,
            email="testuser@example.com",
            username="XXXXXXXX",
            short_description="Test description",
            company=self.company
        )

    def test_company_review_creation(self) -> None:
        """
        Test if company review is created correctly.
        """
        self.assertEqual(self.company_review.choose_rate, 5)
        self.assertEqual(self.company_review.email, "testuser@example.com")
        self.assertEqual(self.company_review.username, "XXXXXXXX")
        self.assertEqual(self.company_review.short_description, "Test description")
        self.assertEqual(self.company_review.company, self.company)

    def test_return_formatted_rate(self):
        """
        Test if return_formatted_rate() method returns correct value.
        """
        self.assertEqual(self.company_review.return_formatted_rate, "5/5")