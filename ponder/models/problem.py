from django.db import models

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