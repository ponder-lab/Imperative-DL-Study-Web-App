from django.db import models

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