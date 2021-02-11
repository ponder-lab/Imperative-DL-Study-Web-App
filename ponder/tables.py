import django_tables2 as tables
from .models import Categorizations, BugFixes

class CategorizationsTable(tables.Table):
    class Meta:
        model = Categorizations
        template_name = "django_tables2/bootstrap-responsive.html"

class BugFixesTable(tables.Table):
    class Meta:
        model = BugFixes
        template_name = "django_tables2/bootstrap-responsive.html"