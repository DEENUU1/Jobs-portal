from django.test import TestCase, CLient
from django.urls import resolve


class StudyViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_study_list_url_resolves(self):
        response = self.client.get('study:study_list')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'study_home_page_list.html')

