from django.test import SimpleTestCase
from ponder.models import Commit, BugFix, Categorization, Categorizer, User
from unittest.mock import patch

class ModelTest(SimpleTestCase):
    # def setUp(self):

    @patch('ponder.models.Commit.objects.get')
    def test_commit_model(self, commit_get):
        commit_get.return_value = Commit(
            id=1,
            project="Mocked-project",
            sha="testsha1234",
            author_email="<test@tester.com>"
        )

        mocked_commit = Commit.objects.get(id=1)

        self.assertEqual(mocked_commit.project, "Mocked-project")
        self.assertEqual(mocked_commit.get_project(), "https://github.com/Mocked-project")
        self.assertEqual(mocked_commit.email_author(), "mailto:test@tester.com")
        self.assertEqual(mocked_commit.get_commit(), "https://github.com/Mocked-project/commit/testsha1234")


    @patch('ponder.models.Commit.objects.values')
    @patch('ponder.models.BugFix.objects.get')
    def test_bugfix_model(self, bugfix_get, commit_values):
        commit_values = Commit.objects.values
        commit_values.filter.return_value = Commit(
            id=1,
            project="Mocked-project",
            sha="testsha1234",
            author_email="<test@tester.com>",
        )

        bugfix_get = BugFix.objects.get
        bugfix_get.return_value = BugFix(
            id=9,
            sha="testsha1234",
        )

        mocked_bugfix = BugFix.objects.get(id=9)

        self.assertIn("testsha1234", mocked_bugfix.get_sha())
        self.assertEqual(mocked_bugfix.get_id(), '9/')

    @patch('ponder.models.Commit.objects.values')
    @patch('ponder.models.User.objects.get')
    @patch('ponder.models.Categorization.objects.get')
    def test_categorization(self, categorization_get, user_get, commit_values):
        user_get = User.objects.get
        user_get.return_value = User(
            id=1,
            username="testuser",
            email="<test@tester.com>"
        )

        commit_values = Commit.objects.values
        commit_values.filter.return_value = Commit(
            id=1,
            project="Mocked-project",
            sha="testsha1234",
            author_email="<test@tester.com>",
        )

        categorization_get = Categorization.objects.get
        categorization_get.return_value = Categorization(
            id=1,
            sha="testsha1234",
            bug_fix=BugFix(
                id=9,
                sha="testsha1234",
            ),
            categorizer=Categorizer(
                name="testuser"
            )
        )

        mocked_categorization = Categorization.objects.get(id=1)

        self.assertIn("testsha1234", mocked_categorization.get_sha())
        self.assertEqual(mocked_categorization.get_absolute_url(), "bug_fixes/9")
        self.assertEqual(mocked_categorization.email_categorizer(), "mailto:<test@tester.com>")