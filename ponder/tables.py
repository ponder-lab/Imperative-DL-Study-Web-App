import django_tables2 as tables
from .models import Categorizations, BugFixes, Categorizers, CommitDetails, Commits, Datasets, ProblemCategories, ProblemCauses, ProblemFixes, ProblemSymptoms

class CategorizationsTable(tables.Table):
    class Meta:
        model = Categorizations
        template_name = "django_tables2/bootstrap-responsive.html"

class BugFixesTable(tables.Table):
    class Meta:
        model = BugFixes
        template_name = "django_tables2/bootstrap-responsive.html"

class CategorizersTable(tables.Table):
    class Meta:
        model = Categorizers
        template_name = "django_tables2/bootstrap-responsive.html"

class CommitDetailsTable(tables.Table):
    class Meta:
        model = CommitDetails
        template_name = "django_tables2/bootstrap-responsive.html"

class CommitsTable(tables.Table):
    class Meta:
        model = Commits
        template_name = "django_tables2/bootstrap-responsive.html"

class DatasetsTable(tables.Table):
    class Meta:
        model = Datasets
        template_name = "django_tables2/bootstrap-responsive.html"

class ProblemCategoriesTable(tables.Table):
    class Meta:
        model = ProblemCategories
        template_name = "django_tables2/bootstrap-responsive.html"

class ProblemCausesTable(tables.Table):
    class Meta:
        model = ProblemCauses
        template_name = "django_tables2/bootstrap-responsive.html"

class ProblemFixesTable(tables.Table):
    class Meta:
        model = ProblemFixes
        template_name = "django_tables2/bootstrap-responsive.html"

class ProblemSymptomsTable(tables.Table):
    class Meta:
        model = ProblemSymptoms
        template_name = "django_tables2/bootstrap-responsive.html"

