from accounts.models import CustomUser
from dashboard.models import (
    Level,
    Position,
    Country,
    Localization,
    Contract,
    Requirements,
    Offer,
    Application,
)
from django.test import TestCase
from offers.models import CompanyReview


class PositionModelTestCase(TestCase):
    """
    Test Case for Position model
    """

    def setUp(self) -> None:
        self.position = Position.objects.create(position_name="Python")

    def test_position_model_new_object_creation_successfully(self) -> None:
        """
        Test creation object of Position model
        :return: None
        """
        self.assertEqual(self.position.position_name, "Python")


class LevelModelTestCase(TestCase):
    """
    Test Case for Level model
    """

    def setUp(self) -> None:
        self.level = Level.objects.create(level_name="Junior")

    def test_level_model_new_object_creation_successfully(self) -> None:
        """
        Test creation object of Level model
        :return: None
        """
        self.assertEqual(self.level.level_name, "Junior")


class CountryModelTestCase(TestCase):
    """
    Test Case for Country model
    """

    def setUp(self) -> None:
        self.country = Country.objects.create(name="Poland")

    def test_country_model_new_object_creation_successfully(self) -> None:
        """
        Test creation object of Country model
        :return: None
        """
        self.assertEqual(self.country.name, "Poland")


class LocalizationModelTestCase(TestCase):
    """
    Test Case for Localization model
    """

    def setUp(self) -> None:
        self.country = Country.objects.create(name="Poland")
        self.localization = Localization.objects.create(
            country=self.country, city="Warsaw"
        )

    def test_localization_model_new_object_creation_successfully(self) -> None:
        """
        Test creation object of Localization model
        :return: None
        """
        self.assertEqual(self.localization.country, self.country)
        self.assertEqual(self.localization.city, "Warsaw")


class ContractModelTestCase(TestCase):
    """
    Test Case for Contract model
    """

    def setUp(self) -> None:
        self.contract = Contract.objects.create(contract_type="B2B")

    def test_contract_model_new_object_creation_successfully(self) -> None:
        """
        Test creation object of Contract model
        :return: None
        """
        self.assertEqual(self.contract.contract_type, "B2B")


class RequirementsModelTestCase(TestCase):
    """
    Test Case for Requirements model
    """

    def setUp(self) -> None:
        self.requirements = Requirements.objects.create(name="Git")

    def test_requirements_model_new_object_creation_successfully(self) -> None:
        """
        Test creation object of Requirements model
        :return: None
        """
        self.assertEqual(self.requirements.name, "Git")


class OfferModelTestCase(TestCase):
    """
    Test case for Offer model
    """

    def setUp(self) -> None:
        self.name = "Junior Python Developer"
        self.position = Position.objects.create(position_name="Python")
        self.level = Level.objects.create(level_name="Junior")
        self.contract = Contract.objects.create(contract_type="B2B")
        self.requirements = Requirements.objects.create(name="Git")
        self.country = Country.objects.create(name="Poland")
        self.localization = Localization.objects.create(
            country=self.country, city="Warsaw"
        )
        self.description = "Junior Python Developer with 10 years exp"
        self.salary_from = 20000
        self.salary_to = 25000
        self.remote = True
        self.custom_user = CustomUser.objects.create(
            role="company", username="Nokia", email="nokia123@wp.pl", password="XXXXXXX"
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
            address="Zielona 4",
        )
        self.offer.contract.add(self.contract)
        self.offer.requirements.add(self.requirements)

    def test_offer_model_new_object_creation_successfully(self) -> None:
        """
        Test creation object of Offer model
        :return: None
        """
        self.assertEqual(self.offer.name, self.name)
        self.assertEqual(self.offer.position, self.position)
        self.assertEqual(self.offer.level, self.level)
        self.assertEqual(list(self.offer.contract.all()), [self.contract])
        self.assertEqual(list(self.offer.requirements.all()), [self.requirements])
        self.assertEqual(self.offer.description, self.description)
        self.assertEqual(self.offer.localization, self.localization)
        self.assertEqual(self.offer.salary_from, self.salary_from)
        self.assertEqual(self.offer.salary_to, self.salary_to)
        self.assertEqual(self.offer.remote, self.remote)
        self.assertEqual(self.offer.company, self.company)

    def test_offer_model_salary_format_method_returns_correct_value_for_specified_object(
        self,
    ) -> None:
        """
        Test salary method from Offer Model
        """
        self.assertEqual(self.offer.salary, "20000 - 25000 PLN")

    def test_offer_model_return_full_address_method_returns_correct_value_for_specified_object(
        self,
    ) -> None:
        """
        Test return_full_address method from Offer Model
        """
        self.assertEqual(self.offer.return_full_address, "Warsaw, Zielona 4")

    def test_offer_model_return_contract_method_returns_correct_value_for_specified_object(
        self,
    ) -> None:
        """
        Test return_contract method from Offer Model
        """
        self.assertEqual(self.offer.return_contract, "B2B")

    def test_offer_model_return_all_requirements_method_returns_correct_value_for_specified_object(
        self,
    ) -> None:
        """
        Test return_all_requirements method from Offer Model
        """
        self.assertEqual(self.offer.return_all_requirements, "Git")


class ApplicationTestCase(TestCase):
    """
    Test Case for Application Model
    """

    def setUp(self) -> None:
        self.offer_model = OfferModelTestCase()
        self.offer_model.setUp()
        self.first_name = "Kacper"
        self.last_name = "Kowalski"
        self.email = "example@example.pl"
        self.phone_number = "+48123123123"
        self.message = "I really want this job"
        self.offer = self.offer_model.offer
        self.expected_pay = 15000
        self.portfolio = "https://www.example.pl/portfolio"
        self.linkedin = "https://www.linkedin.com/in/"

        self.application = Application.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone_number=self.phone_number,
            message=self.message,
            offer=self.offer,
            expected_pay=self.expected_pay,
            portfolio=self.portfolio,
            linkedin=self.linkedin,
        )

    def test_application_model_new_object_successfully_creation(self) -> None:
        """
        Test creation object of Application model
        :return: None
        """
        self.assertEqual(self.application.first_name, self.first_name)
        self.assertEqual(self.application.last_name, self.last_name)
        self.assertEqual(self.application.email, self.email)
        self.assertEqual(self.application.phone_number, self.phone_number)
        self.assertEqual(self.application.message, self.message)
        self.assertEqual(self.application.offer, self.offer)
        self.assertEqual(self.application.expected_pay, self.expected_pay)
        self.assertEqual(self.application.portfolio, self.portfolio)
        self.assertEqual(self.application.linkedin, self.linkedin)

    def test_application_model_return_full_name_method_returns_correct_value_for_specified_object(
        self,
    ) -> None:
        """
        Test return_full_name method from Application Model
        """
        self.assertEqual(self.application.return_full_name, "Kacper Kowalski")


class CompanyReviewTestCase(TestCase):
    def setUp(self) -> None:
        self.company = CustomUser.objects.create(
            username="CompanyX",
            email="company@example.com",
            password="Test123@",
            role="company",
        )
        self.company_review = CompanyReview.objects.create(
            choose_rate=5,
            email="testuser@example.com",
            username="XXXXXXXX",
            short_description="Test description",
            company=self.company,
        )

    def test_company_review_model_new_object_successfully_creation(self) -> None:
        """
        Test if company review is created correctly.
        """
        self.assertEqual(self.company_review.choose_rate, 5)
        self.assertEqual(self.company_review.email, "testuser@example.com")
        self.assertEqual(self.company_review.username, "XXXXXXXX")
        self.assertEqual(self.company_review.short_description, "Test description")
        self.assertEqual(self.company_review.company, self.company)

    def test_company_review_model_return_formatted_rate_method_returns_correct_value_for_specified_object(
        self,
    ):
        """
        Test if return_formatted_rate() method returns correct value.
        """
        self.assertEqual(self.company_review.return_formatted_rate, "5/5")
