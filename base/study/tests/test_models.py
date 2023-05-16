from django.test import TestCase
from study.models import Category, Resources


class StudyModelsTestCase(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name="test")
        self.resources = Resources.objects.create(
            name="test",
            description="Simple test description",
            url="https://google.com",
            date_created="2022-04-24",
            category=self.category,
        )

    def test_category_model_new_object_creation(self):
        self.assertEqual(self.category.name, "test")

    def test_resources_model_new_object_creation(self):
        self.assertEqual(self.resources.name, "test")
        self.assertEqual(self.resources.description, "Simple test description")
        self.assertEqual(self.resources.url, "https://google.com")
        self.assertEqual(self.resources.category, self.category)
