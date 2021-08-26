from django.test import TestCase

# Create your tests here.
#https://adamj.eu/tech/2020/06/15/how-to-unit-test-a-django-form/
#https://stackoverflow.com/questions/7304248/how-should-i-write-tests-for-forms-in-django
#https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.SimpleTestCase.assertFormError
test_cases = [
    {"category_text": "test" }
]


class AddCategorizationFormTests(TestCase):
    def test_all_entered_fields_displayed(self):
        data = test_cases[0]
        response = self.client.post(
            "/ponder/categorizations/add?commit=00a33f7e060caa6616c15003bdac95b7926b76ae", data=test_cases[0])
        self.assertContains(response, 'aaa', html=True)
        self.assertEqual(1, 1)
        
        #assert all input fields are displayed
#assert empty fields are empty value
#assert sha


