# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class BugFix(models.Model):
	sha = models.CharField(max_length=40, blank=False, null=False)
	is_func_fix = models.BooleanField(blank=True, null=True)  # This field type is a guess.
	problem_category = models.ForeignKey('ProblemCategory', models.DO_NOTHING, db_column='problem_category', blank=True, null=True)
	category_comment = models.CharField(max_length=512, blank=True, null=True)
	problem_cause = models.ForeignKey('ProblemCause', models.DO_NOTHING, db_column='problem_cause', blank=True, null=True)
	cause_comment = models.CharField(max_length=512, blank=True, null=True)
	problem_symptom = models.ForeignKey('ProblemSymptom', models.DO_NOTHING, db_column='problem_symptom', blank=True, null=True)
	symptom_comment = models.CharField(max_length=512, blank=True, null=True)
	problem_fix = models.ForeignKey('ProblemFix', models.DO_NOTHING, db_column='problem_fix', blank=True, null=True)
	fix_comment = models.CharField(max_length=512, blank=True, null=True)
	should_discuss = models.BooleanField(blank=True, null=True)

	class Meta:
		managed = False
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
	problem_category = models.ForeignKey('ProblemCategory', models.DO_NOTHING, db_column='problem_category', blank=False, null=False)
	category_comment = models.TextField(blank=True, null=True)
	problem_cause = models.ForeignKey('ProblemCause', models.DO_NOTHING, db_column='problem_cause', blank=False, null=False)
	cause_comment = models.TextField(blank=True, null=True)
	problem_symptom = models.ForeignKey('ProblemSymptom', models.DO_NOTHING, db_column='problem_symptom', blank=False, null=False)
	symptom_comment = models.TextField(blank=True, null=True)
	problem_fix = models.ForeignKey('ProblemFix', models.DO_NOTHING, db_column='problem_fix', blank=False, null=False)
	fix_comment = models.TextField(blank=True, null=True)
	categorizer = models.ForeignKey('Categorizer', models.DO_NOTHING, db_column='categorizer')
	should_discuss = models.BooleanField(blank=True, null=True)
	bug_fix = models.ForeignKey('BugFix', models.DO_NOTHING, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'categorizations'

	def get_sha(self):
		project = Commit.objects.values('project').filter(sha=self.sha)[0]
		return "https://github.com/"+str(project['project'])+"/commit/"+str(self.sha)


class Categorizer(models.Model):
	name = models.CharField(unique=True, max_length=256)
	initials = models.CharField(unique=True, max_length=3)
	user = models.CharField(max_length=256)

	class Meta:
		managed = False
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
		managed = False
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
		managed = False
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
	name = models.CharField(unique=True, max_length=256)
	description = models.CharField(max_length=256)

	class Meta:
		managed = False
		db_table = 'datasets'
	def __str__(self):
		return self.name


class ProblemCategory(models.Model):
	category = models.CharField(unique=True, max_length=512)
	description = models.TextField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'problem_categories'
	def __str__(self):
		return self.category


class ProblemCause(models.Model):
	cause = models.CharField(unique=True, max_length=512)
	description = models.TextField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'problem_causes'

	def __str__(self):
		return self.cause


class ProblemFix(models.Model):
	fix = models.CharField(unique=True, max_length=512)

	class Meta:
		managed = False
		db_table = 'problem_fixes'
	def __str__(self):
		return self.fix


class ProblemSymptom(models.Model):
	symptom = models.CharField(max_length=512)

	class Meta:
		managed = False
		db_table = 'problem_symptoms'

	def __str__(self):
		return self.symptom


class Repository(models.Model):
	project = models.ForeignKey(Commit, models.DO_NOTHING, db_column='project')
	user = models.CharField(max_length=25)
	forks = models.IntegerField()
	stars = models.IntegerField()
	watchers = models.IntegerField()
	open_issues = models.IntegerField()
	is_engineered_project = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'repositories'

	def __str__(self):
		return self.project
