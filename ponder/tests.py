from django.test import TestCase
import django
django.setup()

from ponder.models import Categorization, Categorizer, Commit, Dataset, ProblemCategory, ProblemCause, ProblemSymptom, ProblemFix
from django.contrib.auth.models import User
from ponder.forms import CategorizationForm

from django.db import IntegrityError
# Create your tests here.

class AddCategorizationFormTests(TestCase):
    '''
    @classmethod
    def setUpTestData(self):
        newCategory1 = ProblemCategory.objects.create(category='category1', description='test')
        newCategory2 = ProblemCategory.objects.create(category='category2', description='test')
        newCategory3 = ProblemCategory.objects.create(category='category3', description='test')
        newCategory4 = ProblemCategory.objects.create(category='category4', description='test')
        newCategory5 = ProblemCategory.objects.create(category='category5', description='test')
        newCause = ProblemCause.objects.create(cause='test', description='test')
        newSymptom = ProblemSymptom.objects.create(symptom='test', description='test')
        newFix = ProblemFix.objects.create(fix='test', description='test')
    
    # These 2 tests should not be part of the insertion form validation. The validity of the sha and the user can be tested when the 
    # commits table and the categorizations table are rendered, respectively.
    def test_sha_not_null(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha=None, data={}, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because sha is null

    def test_categorizer_not_null(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='',symptom_description='',sha='0000000', data={}, user=None)
        self.assertFalse(form.is_valid()) # The form should not be valid because categorizer is null
    '''
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
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data=data, user='testUser')
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
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data=data, user='testUser')
        for field in data:
            self.assertEqual(data[field], form.data[field])

    # Check constraint is at https://gist.github.com/khatchad/09f0c8d1ca6e0f23b0b9bbf5c62ac8f9#file-commit_categorizations-sql-L32.
    #If the func fix is null, then we don't need any of the other fields populated.
    def test_null_func_fix(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data={"is_func_fix": None}, user='testUser')
        self.assertTrue(form.is_valid()) # The form should be valid.
        self.assertNotIn("is_func_fix", form.errors) # There should be no errors.

    #If the id of the problem category is 1, then we don't need any of the other fields populated.
    def test_problem_category_id_1(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data={"is_func_fix": True, "problem_category": "1"}, user='testUser')
        self.assertTrue(form.is_valid()) # The form should be valid.
        self.assertNotIn("problem_category", form.errors) # There should be no errors.

    #If the id of the problem category is 2, then we don't need any of the other fields populated.
    def test_problem_category_id_2(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data={"is_func_fix": True, "problem_category": "2"}, user='testUser')
        self.assertTrue(form.is_valid()) # The form should be valid.
        self.assertNotIn("problem_category", form.errors) # There should be no errors.

    #If the id of the problem category is 5, then we don't need any of the other fields populated.
    def test_problem_category_id_5(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data={"is_func_fix": True, "problem_category": "5"}, user='testUser')
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
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data=data, user='testUser')
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
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because is func fix is not null and problem category is null
        self.assertEqual(form.errors["problem_category"], ['This field is required. Select an existing problem category or enter a new one.'])
    
    #Case when is func fix is not null, problem caretegory id is not 1, 2 or 5, and problem cause is missing
    def test_problem_cause_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_category": "3", #not 1, 2, or 5
            "problem_symptom": "1",
            "problem_fix": "1",
            "should_discuss": True
        }
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because problem cause is missing
        self.assertEqual(form.errors["problem_cause"], ['This field is required. Select an existing problem cause or enter a new one.'])

    #Case when is func fix is not null, problem caretegory id is not 1, 2 or 5, and problem symptom is missing
    def test_problem_symptom_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_category": "3", #not 1, 2, or 5
            "problem_cause": "1",
            "problem_fix": "1",
            "should_discuss": True
        }
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because problem symptom is missing
        self.assertEqual(form.errors["problem_symptom"], ['This field is required. Select an existing problem symptom or enter a new one.'])

    #Case when is func fix is not null, problem caretegory id is not 1, 2 or 5, and problem fix is missing
    def test_problem_fix_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_category": "3", #not 1, 2, or 5
            "problem_cause": "1",
            "problem_symptom": "1",
            "should_discuss": True
        }
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because problem fix is missing
        self.assertEqual(form.errors["problem_fix"], ['This field is required. Select an existing problem fix or enter a new one.'])
    '''
    #Case when is func fix is not null, problem caretegory id is not 1, 2 or 5, and should discuss is missing
    def test_should_discuss_not_null(self):
        data = {
            "is_func_fix": True, #not null
            "problem_category": "3", #not 1, 2, or 5
            "problem_cause": "1",
            "problem_symptom": "1",
            "problem_fix": "1"
        }
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data=data, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid because should dicuss is missing
        self.assertEqual(form.errors["should_dicuss"], ["Should_discuss can not be null."])
    '''
    #issue: https://github.com/ponder-lab/Imperative-DL-Study-Web-App/issues/103
    #Case when an existing category is selected and a new category is entered
    def test_problem_category_not_selected_and_entered(self):
        form = CategorizationForm(category_text='test', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data={"is_func_fix": True, "problem_category": "1"}, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid.
        self.assertEqual(form.errors["problem_category"], ["Choose only one option. Either select an existing problem category or enter a new one."])

    #Case when an existing problem cause is selected and a new problem cause is entered
    def test_problem_cause_not_selected_and_entered(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='test', cause_description='',fix_text='',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data={"is_func_fix": True, "problem_cause": "1"}, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid.
        self.assertEqual(form.errors["problem_cause"], ["Choose only one option. Either select an existing problem cause or enter a new one."])

    #Case when an existing problem symptom is selected and a new problem symptom is entered
    def test_problem_symptom_not_selected_and_entered(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='',fix_description='', \
            symptom_text='test', symptom_description='',sha='0000000', data={"is_func_fix": True, "problem_symptom": "1"}, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid.
        self.assertEqual(form.errors["problem_symptom"], ["Choose only one option. Either select an existing problem symptom or enter a new one."])

    #Case when an existing problem fix is selected and a new problem fix is entered
    def test_problem_fix_not_selected_and_entered(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='test',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data={"is_func_fix": True, "problem_fix": "1"}, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid.
        self.assertEqual(form.errors["problem_fix"], ["Choose only one option. Either select an existing problem fix or enter a new one."])

    #Case when there is a problem category but func fix is false
    def test_category_not_null_and_func_fix_null(self):
        form = CategorizationForm(category_text='', category_description='', cause_text='', cause_description='',fix_text='test',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data={"is_func_fix": False, "problem_category": "1"}, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid.
        self.assertEqual(form.errors["is_func_fix"], ["This field should be checked. An existing problem category indicates a bug fix."])
    
    #Case when there is a problem category text but func fix is false
    def test_category_text_not_null_and_func_fix_null(self):
        form = CategorizationForm(category_text='test', category_description='', cause_text='', cause_description='',fix_text='test',fix_description='', \
            symptom_text='', symptom_description='',sha='0000000', data={"is_func_fix": False}, user='testUser')
        self.assertFalse(form.is_valid()) # The form should not be valid.
        self.assertEqual(form.errors["is_func_fix"], ["This field should be checked. An existing problem category indicates a bug fix."])

class CategorizerTests(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create two new Django users.
        self.user1 = User.objects.create_user(username='testUser1', password='testpassword')
        self.user2 = User.objects.create_user(username='testUser2', password='testpassword')
    
    # Case when a new categorizer is being added when the given name already exists in the table.
    def test_same_name(self):
        # Make sure there are no other categorizers.
        Categorizer.objects.all().delete()
        
        # Create a categorizer John Smith.
        Categorizer.objects.create(name='John Smith', initials='JS', user=self.user1)
        
        # Second categorizer is inserted with the same name and different initials and username.
        Categorizer.objects.create(name='John Smith', initials='AB', user=self.user2)
        
        # Both testUser1 and testUser2 with the name "John Smith" should be in the table because two categorziers can have the same name
        self.assertTrue(Categorizer.objects.filter(user='testUser1').exists())
        self.assertTrue(Categorizer.objects.filter(user='testUser2').exists())

    # case when a new categorizer is being added when the given initial already exists in the table
    def test_same_initials(self):
        Categorizer.objects.all().delete()
        Categorizer.objects.create(name='John Smith', initials='JS', user=self.user1)
        #second categorizer is inserted with the same initials and different name and username.
        Categorizer.objects.create(name='Jane Scott', initials='JS', user=self.user2)
        #both testUser1 and testUser2 with the initials "JS" should be in the table because two categorziers can have the same initials
        self.assertTrue(Categorizer.objects.filter(user='testUser1').exists())
        self.assertTrue(Categorizer.objects.filter(user='testUser2').exists())

    #case when a new categorizer is being added when the given user already exists in the table
    def test_same_user(self):
        Categorizer.objects.all().delete()
        Categorizer.objects.create(name='John Smith', initials='JS', user=self.user1)
        #the same user is inserted again with different name and initials
        #expecting an exaception when Categorizer.objects.create(name='Michelle Reed', initials='MR', user=self.user1) is called
        self.assertRaises(IntegrityError, Categorizer.objects.create, name='Michelle Reed', initials='MR', user=self.user1)
