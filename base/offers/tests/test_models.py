from django.test import TestCase
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
from accounts.models import CustomUser


class PositionModelTestCase(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            position_name = "Python"
        )
    
    def test_position_model_creation(self):
        self.assertEqual(
            self.position.position_name, "Python"
        )


class LevelModelTestCase(TestCase):
    def setUp(self) -> None:
        self.level = Level.objects.create(
            level_name = "Junior"
        )
    
    def test_level_model_creation(self):
        self.assertEqual(
            self.level.level_name, "Junior"
        )


class CountryModelTestCase(TestCase):
    def setUp(self) -> None:
        self.country = Country.objects.create(
            name = "Poland"
        )
    
    def test_country_model_creation(self):
        self.assertEqual(
            self.country.name, "Poland"
        )


class LocalizationModelTestCase(TestCase):
    def setUp(self) -> None:
        self.country = Country.objects.create(
            name = "Poland"
        )
        self.localization = Localization.objects.create(
            country = self.country,
            city = "Warsaw"
        )

    def test_localization_model_creation(self):
        self.assertEqual(
            self.localization.country, self.country
        )
        self.assertEqual(
            self.localization.city, "Warsaw"
        )


class ContractModelTestCase(TestCase):
    def setUp(self) -> None:
        self.contract = Contract.objects.create(
            contract_type = "B2B"
        )
    
    def test_contract_model_creation(self):
        self.assertEqual(
            self.contract.contract_type, "B2B"
        )
