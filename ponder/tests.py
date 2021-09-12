from django.test import TestCase
import django
django.setup()

from ponder.models import Categorization, Categorizer, Commit, Dataset, ProblemCategory, ProblemCause, ProblemSymptom, ProblemFix
#from django.test import Client
from django.contrib.auth.models import User
from ponder.forms import CategorizationForm
# Create your tests here.

class AddCategorizationFormTests(TestCase):
    @classmethod
    def setUpTestData(self):
        #user = User.objects.create_user(username='testUser', password='testPassword')
        #newCategorizer = Categorizer.objects.create(name='test', initials='t', user='testUser')
        #newDataset = Dataset.objects.create()
        #newCommit = Commit.objects.create(sha='00f703fb6796b52c8f925ff105f058981f91cb02', dataset=newDataset)
        newCategory1 = ProblemCategory.objects.create(category='category1', description='test')
        newCategory2 = ProblemCategory.objects.create(category='category2', description='test')
        newCategory3 = ProblemCategory.objects.create(category='category3', description='test')
        newCategory4 = ProblemCategory.objects.create(category='category4', description='test')
        newCategory5 = ProblemCategory.objects.create(category='category5', description='test')
        newCause = ProblemCause.objects.create(cause='test', description='test')
        newSymptom = ProblemSymptom.objects.create(symptom='test', description='test')
        newFix = ProblemFix.objects.create(fix='test', description='test')
        #self.data = test_cases[0]
        #self.client = Client()
        #self.client.login(username='testUser', password='testPassword')
        #self.form = CategorizationForm(data=self.data, sha='00f703fb6796b52c8f925ff105f058981f91cb02', user='testUser')
        #self.client.post("/ponder/categorizations/add?commit=00f703fb6796b52c8f925ff105f058981f91cb02", self.data)
        #self.newCategorization = Categorization.objects.all()[0]

    def test_sha_not_null(self):
        form = CategorizationForm(sha=None, data={}, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because sha is null

    def test_categorizer_not_null(self):
        form = CategorizationForm(sha='0000000', data={}, user=None)
        self.assertFalse(form.is_valid()) # The form should not be valid because categorizer is null

    #Test that all the fields in test data exist in the form
    def test_all_test_data_fields_exist_in_form(self):
        data = {
            "is_func_fix": True,
            "problem_category": "1",
            'category_comment': "test",
            "problem_cause": "1",
            'cause_comment': "test",
            "problem_symptom": "1",
            'symptom_comment': "test",
            "problem_fix": "1",
            "fix_comment": "test",
            "should_discuss": True
        }
        form = CategorizationForm(sha='0000000', data=data, user='testUser')
        for field in data:
            self.assertIn(field, form.data)
    
    # Test that all the test data was correctly populated in the form.
    def test_all_entered_fields_are_stored_correctly_in_form(self):
        data = {
            "is_func_fix": True,
            "problem_category": "1",
            'category_comment': "test",
            "problem_cause": "1",
            'cause_comment': "test",
            "problem_symptom": "1",
            'symptom_comment': "test",
            "problem_fix": "1",
            "fix_comment": "test",
            "should_discuss": True
        }
        form = CategorizationForm(sha='0000000', data=data, user='testUser')
        for field in data:
            self.assertEqual(data[field], form.data[field])

    # Check constraint is at https://gist.github.com/khatchad/09f0c8d1ca6e0f23b0b9bbf5c62ac8f9#file-commit_categorizations-sql-L32.
    #If the func fix is null, then we don't need any of the other fields populated.
    def test_null_func_fix(self):
        form = CategorizationForm(sha='0000000', data={"is_func_fix": None}, user='testUser')
        self.assertTrue(form.is_valid()) # The form should be valid.
        self.assertNotIn("is_func_fix", form.errors) # There should be no errors.

    #If the id of the problem category is 1, then we don't need any of the other fields populated.
    def test_problem_category_id_1(self):
        form = CategorizationForm(sha='0000000', data={"problem_category": "1"}, user='testUser')
        self.assertTrue(form.is_valid()) # The form should be valid.
        self.assertNotIn("problem_category", form.errors) # There should be no errors.

    #If the id of the problem category is 2, then we don't need any of the other fields populated.
    def test_problem_category_id_2(self):
        form = CategorizationForm(sha='0000000', data={"problem_category": "2"}, user='testUser')
        self.assertTrue(form.is_valid()) # The form should be valid.
        self.assertNotIn("problem_category", form.errors) # There should be no errors.

    #If the id of the problem category is 5, then we don't need any of the other fields populated.
    def test_problem_category_id_5(self):
        form = CategorizationForm(sha='0000000', data={"problem_category": "5"}, user='testUser')
        self.assertTrue(form.is_valid()) # The form should be valid.
        self.assertNotIn("problem_category", form.errors) # There should be no errors.
 
    '''
    If the func fix is not null and the problem category is not 1, 2, or 5, then 
    problem cateogry, problem cause, problem symptom, and problem fix, and should
    dicuss must not be null.
    '''
    #Case when all required fields are not null
    def test_required_fields_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_category": "3", #not 1, 2, or 5
            "problem_cause": "1",
            "problem_symptom": "1",
            "problem_fix": "1",
            "should_discuss": True
        }
        form = CategorizationForm(sha='0000000', data=data, user='testUser')
        self.assertTrue(form.is_valid()) # The form should be valid
        self.assertEqual(form.errors, {}) # There should be no errors

    #Case when is func fix is not null and problem category is missing
    def test_problem_cause_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_cause": "1",
            "problem_symptom": "1",
            "problem_fix": "1",
            "should_discuss": True
        }
        form = CategorizationForm(sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because is func fix is not null and problem category is null
        self.assertEqual(form.errors["problem_category"], ["Problem category can not be null."])
    
    #Case when is func fix is not null, problem caretegory id is not 1, 2 or 5, and problem cause is missing
    def test_problem_cause_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_category": "3", #not 1, 2, or 5
            "problem_symptom": "1",
            "problem_fix": "1",
            "should_discuss": True
        }
        form = CategorizationForm(sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because problem cause is missing
        self.assertEqual(form.errors["problem_cause"], ["Problem cause can not be null."])

    #Case when is func fix is not null, problem caretegory id is not 1, 2 or 5, and problem symptom is missing
    def test_problem_symptom_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_category": "3", #not 1, 2, or 5
            "problem_cause": "1",
            "problem_fix": "1",
            "should_discuss": True
        }
        form = CategorizationForm(sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because problem symptom is missing
        self.assertEqual(form.errors["problem_symptom"], ["Problem symptom can not be null."])

    #Case when is func fix is not null, problem caretegory id is not 1, 2 or 5, and problem fix is missing
    def test_problem_fix_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_category": "3", #not 1, 2, or 5
            "problem_cause": "1",
            "problem_symptom": "1",
            "should_discuss": True
        }
        form = CategorizationForm(sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because problem fix is missing
        self.assertEqual(form.errors["problem_fix"], ["Problem fix can not be null."])

    #Case when is func fix is not null, problem caretegory id is not 1, 2 or 5, and should discuss is missing
    def test_should_discuss_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_category": "3", #not 1, 2, or 5
            "problem_cause": "1",
            "problem_symptom": "1",
            "problem_fix": "1"
        }
        form = CategorizationForm(sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because should dicuss is missing
        self.assertEqual(form.errors["should_dicuss"], ["Should_discuss can not be null."])