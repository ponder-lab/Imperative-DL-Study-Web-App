from django.db import models
from .commit import Commit

class BugFix(models.Model):
    sha = models.CharField(max_length=40, blank=False, null=False, verbose_name='SHA')
    is_func_fix = models.BooleanField()
    problem_category = models.ForeignKey('ProblemCategory', models.DO_NOTHING, db_column='problem_category', blank=True, null=True)
    category_comment = models.TextField(blank=True, null=True)
    problem_cause = models.ForeignKey('ProblemCause', models.DO_NOTHING, db_column='problem_cause', blank=True, null=True)
    cause_comment = models.TextField(blank=True, null=True)
    problem_symptom = models.ForeignKey('ProblemSymptom', models.DO_NOTHING, db_column='problem_symptom', blank=True, null=True)
    symptom_comment = models.TextField(blank=True, null=True)
    problem_fix = models.ForeignKey('ProblemFix', models.DO_NOTHING, db_column='problem_fix', blank=True, null=True)
    fix_comment = models.TextField(blank=True, null=True)
    should_discuss = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'bug_fixes'

    def get_id(self):
        return "%i/" % self.id

    def __str__(self):
        return "%s" % self.id

    def get_sha(self):
        project = Commit.objects.values('project').filter(sha=self.sha)[0]
        return "https://github.com/"+str(project['project'])+"/commit/"+str(self.sha)