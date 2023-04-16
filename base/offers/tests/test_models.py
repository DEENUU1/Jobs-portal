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
