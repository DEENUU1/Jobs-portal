from accounts.models import CustomUser
from django.test import TestCase
from offers.models import (
    CompanyReview,
)


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