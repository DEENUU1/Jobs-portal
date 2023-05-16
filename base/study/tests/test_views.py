from django.test import TestCase, Client
from django.urls import reverse


class StudyViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_study_list_view_get_method_returns_200_status_code(self):
        response = self.client.get(reverse("study:study_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "study_home_page_list.html")
