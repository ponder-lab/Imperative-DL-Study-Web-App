from django.db import models
from django.contrib.auth.models import User

class BugFix(models.Model):
	sha = models.CharField(max_length=40, blank=False, null=False)
	is_func_fix = models.BooleanField() # This is a required field.
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
	user = models.CharField(max_length=254)

	class Meta:
		db_table = 'categorizers'

	def __str__(self):
		return self.user


class CommitDetail(models.Model):
	sha = models.CharField(max_length=40, blank=False, null=False)
	language = models.CharField(max_length=2, blank=True, null=True)
	file_name = models.CharField(max_length=100, blank=True, null=True)
	is_test = models.IntegerField(blank=True, null=True)
	method_name = models.CharField(max_length=51, blank=True, null=True)
	tf_function_adds = models.IntegerField(db_column='tf.function_adds', blank=True, null=True)  # Field renamed to remove unsuitable characters.
	tf_function_dels = models.IntegerField(db_column='tf.function_dels', blank=True, null=True)  # Field renamed to remove unsuitable characters.
	total_adds = models.IntegerField(blank=True, null=True)
	total_dels = models.IntegerField(blank=True, null=True)
	warning_alert = models.IntegerField(blank=True, null=True)

	class Meta:
		db_table = 'commit_details'


class Commit(models.Model):
	project = models.CharField(max_length=41)
	sha = models.CharField(max_length=40, blank=False, null=False)
	author = models.CharField(max_length=25, blank=True, null=True)
	author_email = models.CharField(max_length=47, blank=True, null=True)
	commit_date = models.DateField(blank=True, null=True)
	dataset = models.ForeignKey('Dataset', models.DO_NOTHING, db_column='dataset')
	rounds = models.IntegerField(blank=True, null=True)

	class Meta:
		db_table = 'commits'

	def __str__(self):
		return self.sha

	def get_project(self):
		return "https://github.com/"+str(self.project)
	
	def email_author(self):
		return "mailto:" + self.author_email.strip('<>') # remove brackets per #33.
  
	def get_commit(self):
		return "https://github.com/"+str(self.project)+"/commit/"+str(self.sha)


class Dataset(models.Model):
	#id = models.OneToOneField(Commit, models.DO_NOTHING, db_column='id', primary_key=True)
	name = models.CharField(unique=True, max_length=254)
	description = models.CharField(max_length=254)

	class Meta:
		db_table = 'datasets'

	def __str__(self):
		return self.name


class ProblemCategory(models.Model):
	category = models.CharField(unique=True, max_length=254)
	description = models.TextField(blank=True, null=True)

	class Meta:
		db_table = 'problem_categories'

	def __str__(self):
		return self.category


class ProblemCause(models.Model):
	cause = models.CharField(unique=True, max_length=254)
	description = models.TextField(blank=True, null=True)

	class Meta:
		db_table = 'problem_causes'

	def __str__(self):
		return self.cause


class ProblemFix(models.Model):
	fix = models.CharField(unique=True, max_length=254)
	description = models.TextField(blank=True, null=True)

	class Meta:
		db_table = 'problem_fixes'

	def __str__(self):
		return self.fix


class ProblemSymptom(models.Model):
	symptom = models.CharField(max_length=254)
	description = models.TextField(blank=True, null=True)

	class Meta:
		db_table = 'problem_symptoms'

	def __str__(self):
		return self.symptom


class Repository(models.Model):
	project = models.CharField(max_length=41)
	user = models.CharField(max_length=25)
	forks = models.IntegerField()
	stars = models.IntegerField()
	watchers = models.IntegerField()
	open_issues = models.IntegerField()
	is_engineered_project = models.IntegerField(blank=True, null=True)

	class Meta:
		db_table = 'repositories'

	def __str__(self):
		return self.project
