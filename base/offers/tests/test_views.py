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


class OffersViewTestCase(TestCase):
    """
    Test case for views related to job offers.
    """
    def setUp(self) -> None:
        """
        Set up the test case by creating users, positions, levels, contracts, requirements, offers, and applications.
        """
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            role="user",
            first_name="user",
            last_name="user",
            username="user",
            email="user@example.com",
            password="Test123@"
        )
        self.company = CustomUser.objects.create_user(
            role="company",
            username="company",
            email="company@example.com",
            password="Test123@"
        )
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
        self.application = Application.objects.create(
            first_name="XXX",
            last_name="XXX",
            email="XXXXXXXXX@example.com",
            phone_number="+48123456789",
            offer=self.offer,
            expected_pay="30000",
            portfolio="https://www.example.com",
            linkedin="https://www.linkedin.com/in/xxxxx",
        )