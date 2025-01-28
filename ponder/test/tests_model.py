from django.test import SimpleTestCase

class ModelTest(SimpleTestCase):
    # def setUp(self):

    def test_self(self):
        self.assertEqual("Hello", "Hello")