from django.db import models
from django.contrib.auth.models import User
from .commit import Commit

class Categorization(models.Model):
    sha = models.CharField(max_length=40, blank=False, null=False)
    is_func_fix = models.BooleanField()
    func_fix_comment = models.TextField(blank=True, null=True)
    problem_category = models.ForeignKey('ProblemCategory', models.DO_NOTHING, db_column='problem_category', blank=True, null=True)
    category_comment = models.TextField(blank=True, null=True)
    problem_cause = models.ForeignKey('ProblemCause', models.DO_NOTHING, db_column='problem_cause', blank=True, null=True)
    cause_comment = models.TextField(blank=True, null=True)
    problem_symptom = models.ForeignKey('ProblemSymptom', models.DO_NOTHING, db_column='problem_symptom', blank=True, null=True)
    symptom_comment = models.TextField(blank=True, null=True)
    problem_fix = models.ForeignKey('ProblemFix', models.DO_NOTHING, db_column='problem_fix', blank=True, null=True)
    fix_comment = models.TextField(blank=True, null=True)
    categorizer = models.ForeignKey('Categorizer', models.DO_NOTHING, db_column='categorizer')
    should_discuss = models.BooleanField(blank=True, null=True)
    bug_fix = models.ForeignKey('BugFix', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'categorizations'

    def get_sha(self):
        project = Commit.objects.values('project').filter(sha=self.sha)[0]
        return "https://github.com/"+str(project['project'])+"/commit/"+str(self.sha)

    def get_absolute_url(self):
        return "bug_fixes/"+str(self.bug_fix)

    def email_categorizer(self):
        user = User.objects.get(username=self.categorizer)
        return "mailto:" + user.email


class Categorizer(models.Model):
    name = models.CharField(max_length=254)
    initials = models.CharField(unique=True, max_length=3)
    user = models.OneToOneField(User, to_field="username", db_column='user', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'categorizers'

    def __str__(self):
        return str(self.user)