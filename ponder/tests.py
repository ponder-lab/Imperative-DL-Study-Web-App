from django.test import TestCase
import django
django.setup()

from ponder.models import Categorization, Categorizer, Commit, Dataset, ProblemCategory, ProblemCause, ProblemSymptom, ProblemFix
from django.test import Client
from django.contrib.auth.models import User
from ponder.forms import CategorizationForm
# Create your tests here.
test_cases = [
    {
        'func_fix_comment': '',
        'problem_category': '1',
        'category_text': 'test',
        'category_description': '',
        'category_comment': 'test test test',
        'problem_cause': '1',
        'cause_text': '',
        'cause_description': '',
        'cause_comment': '',
        'problem_symptom': '1',
        'symptom_text': '',
        'symptom_description': '',
        'symptom_comment': '',
        'problem_fix': '',
        'fix_text': '1',
        'fix_description': '',
        'fix_comment': '',
    }
]

class AddCategorizationFormTests(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(username='testUser', password='testPassword')
        newCategorizer = Categorizer.objects.create(name='test', initials='t', user='testUser')
        newDataset = Dataset.objects.create()
        newCommit = Commit.objects.create(sha='00f703fb6796b52c8f925ff105f058981f91cb02', dataset=newDataset)
        newCategory = ProblemCategory.objects.create(category='test', description='test')
        newCause = ProblemCause.objects.create(cause='test', description='test')
        newSymptom = ProblemSymptom.objects.create(symptom='test', description='test')
        newFix = ProblemFix.objects.create(fix='test', description='test')
        self.data = test_cases[0]
        self.client = Client()
        self.client.login(username='testUser', password='testPassword')
        self.form = CategorizationForm(data=self.data, sha='00f703fb6796b52c8f925ff105f058981f91cb02', user='testUser')
        self.client.post("/ponder/categorizations/add?commit=00f703fb6796b52c8f925ff105f058981f91cb02", self.data)
        self.newCategorization = Categorization.objects.all()[0]

    def test_sha_not_null(self):
        self.assertIsNotNone(self.newCategorization.sha)

    def test_categorizer_not_null(self):
        self.assertIsNotNone(self.newCategorization.categorizer)

    def test_all_test_data_fields_exist_in_form(self):
        for field in self.data:
            if len(self.data[field]) >= 1:
                self.assertTrue(field in self.form.data and len(self.form.data[field]) >= 1)
    
    # Test that all the test data was correctly populated in the form.
    def test_all_entered_fields_are_stored_correctly_in_form(self):
        for field in self.data:
            if len(self.data[field]) >= 1:
                self.assertEqual(self.data[field], self.form.data[field])
    """
    def test_constraints(self):
        if ((self.data.get('is_func_fix') == 'on' 
        or self.data.get('problem_category') == '1' 
        or self.data.get('problem_category') == '2' 
        or self.data.get('problem_category') == '5')
        or (len(self.data.get('problem_category')) >= 1
        and len(self.data.get('problem_cause')) >= 1
        and len(self.data.get('problem_symptom')) >= 1
        and len(self.data.get('problem_fix')) >= 1
        and self.data.get('should_discuss') is not None
        and len(self.data.get('should_discuss')) >= 1)):
            self.assertTrue(self.form.is_valid())
        else:
            self.assertFalse(self.form.is_valid())
    """

    # Check constraint is at https://gist.github.com/khatchad/09f0c8d1ca6e0f23b0b9bbf5c62ac8f9#file-commit_categorizations-sql-L32.
    
    """
    If the func fix is null, then we don't need any of the other fields populated.
    """
    def test_null_func_fix:
        form = CategorizationForm(sha='0000000', data={"is_func_fix": null})
        self.assert(form.is_valid()) # The form should be valid.
        self.assert(form.errors["is_func_fix"], []) # There should be no errors.
