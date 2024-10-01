from django.test import TestCase


# Create your tests here.
class ViewTests(TestCase):
    def test_health_check(self):
        response = self.client.get("/health-check")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ok")
