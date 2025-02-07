from django.db import models

class CommitDetail(models.Model):
    sha = models.CharField(max_length=40, blank=False, null=False, verbose_name='SHA')
    language = models.CharField(max_length=2, blank=True, null=True)
    file_name = models.CharField(max_length=100, blank=True, null=True)
    is_test = models.IntegerField(blank=True, null=True)
    method_name = models.CharField(max_length=51, blank=True, null=True)
    tf_function_adds = models.IntegerField(db_column='tf.function_adds', blank=True, null=True)
    tf_function_dels = models.IntegerField(db_column='tf.function_dels', blank=True, null=True)
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
        return "mailto:" + self.author_email.strip('<>')

    def get_commit(self):
        return "https://github.com/"+str(self.project)+"/commit/"+str(self.sha)


class Dataset(models.Model):
    name = models.CharField(unique=True, max_length=254)
    description = models.CharField(max_length=254)

    class Meta:
        db_table = 'datasets'

    def __str__(self):
        return self.name