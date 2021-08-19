import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import Categorization, BugFix, Categorizer, CommitDetail, Commit, Dataset, ProblemCategory, ProblemCause, ProblemFix, ProblemSymptom
from django.utils.html import format_html
import re

def activateLinks(text):
		pattern = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
		result = ""
		idx = 0
		for match in pattern.finditer(text):
			start, end = match.start(0), match.end(0)
			result = format_html("{}{}<a href='{}'>{}</a>", result, text[idx:start], text[start:end], text[start:end])
			idx = end
		result = format_html("{}{}", result, text[idx:])
		return result

class CategorizationsTable(tables.Table):
	class Meta:
		model = Categorization
		template_name = "django_tables2/bootstrap-responsive.html"

class BugFixesTable(tables.Table):
	id = tables.Column(linkify=lambda record: record.get_id())
	sha = tables.Column(linkify=lambda record: record.get_sha(), attrs={"a": {"target": "_blank"}})
	problem_category = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_category.description}})
	problem_cause = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_cause.description}})
	problem_symptom = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_symptom.description}})
	problem_fix = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_fix.description}})
	class Meta:
		model = BugFix
		template_name = "django_tables2/bootstrap-responsive.html"

	def render_category_comment(self, value):
		return activateLinks(value)
	
	def render_cause_comment(self, value):
		return activateLinks(value)

	def render_symptom_comment(self, value):
		return activateLinks(value)

	def render_fix_comment(self, value):
		return activateLinks(value)

class CategorizersTable(tables.Table):
	class Meta:
		model = Categorizer
		template_name = "django_tables2/bootstrap-responsive.html"

class CommitDetailsTable(tables.Table):
	class Meta:
		model = CommitDetail
		template_name = "django_tables2/bootstrap-responsive.html"

class CommitsTable(tables.Table):
	add_form = TemplateColumn(template_name='ponder/add_a_categorization.html')
	go_to_details = TemplateColumn(template_name='ponder/go_to_details.html', verbose_name="ID")
	project = tables.Column(linkify=lambda record: record.get_project(), attrs={"a": {"target": "_blank"}})
	author = tables.Column(linkify=lambda record: record.email_author())
	sha = tables.Column(linkify=lambda record: record.get_commit(), attrs={"a": {"target": "_blank"}})
	dataset = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.dataset.description}})
	class Meta:
		model = Commit
		exclude = ('author_email','id')
		template_name = "django_tables2/bootstrap-responsive.html"
		sequence = ('go_to_details','project', 'sha', 'author', 'commit_date', 'dataset', 'rounds', 'add_form')

class Categorizations_FilterTable(tables.Table):
	sha = tables.Column(linkify=lambda record: record.get_sha(), attrs={"a": {"target": "_blank"}})
	bug_fix = tables.Column(linkify=True)
	categorizer = tables.Column(linkify=lambda record: record.email_categorizer())
	problem_category = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_category.description}})
	problem_cause = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_cause.description}})
	problem_symptom = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_symptom.description}})
	problem_fix = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_fix.description}})
	Round = TemplateColumn('{{}}')
	class Meta:
		model = Categorization
		template_name = "django_tables2/bootstrap-responsive.html"
		
	def render_Round(self, record):
		rounds = Commit.objects.values_list('rounds', flat=True).filter(sha=record.sha)[0]
		return rounds

	def render_func_fix_comment(self, value):
		return activateLinks(value)

	def render_category_comment(self, value):
		return activateLinks(value)

	def render_cause_comment(self, value):
		return activateLinks(value)
	
	def render_symptom_comment(self, value):
		return activateLinks(value)
	
	def render_fix_comment(self, value):
		return activateLinks(value)

class BugFixes_FilterTable(tables.Table):
	sha = tables.Column(linkify=lambda record: record.get_sha(), attrs={"a": {"target": "_blank"}})
	categorizer = tables.Column(linkify=lambda record: record.email_categorizer())
	problem_category = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_category.description}})
	problem_cause = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_cause.description}})
	problem_symptom = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_symptom.description}})
	problem_fix = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_fix.description}})
	class Meta:
		model = Categorization
		exclude = ('bug_fix',)
		template_name = "django_tables2/bootstrap-responsive.html"

class DatasetsTable(tables.Table):
	class Meta:
		model = Dataset
		template_name = "django_tables2/bootstrap-responsive.html"
	
class ProblemCategoriesTable(tables.Table):
	id = tables.Column(linkify=True)
	category = tables.Column(linkify=True)
	description = tables.Column(linkify=True)
	class Meta:
		model = ProblemCategory
		template_name = "django_tables2/bootstrap-responsive.html"

class ProblemCausesTable(tables.Table):
	id = tables.Column(linkify=True)
	cause = tables.Column(linkify=True)
	description = tables.Column(linkify=True)
	class Meta:
		model = ProblemCause
		template_name = "django_tables2/bootstrap-responsive.html"

class ProblemFixesTable(tables.Table):
	id = tables.Column(linkify=True)
	fix = tables.Column(linkify=True)
	class Meta:
		model = ProblemFix
		template_name = "django_tables2/bootstrap-responsive.html"

class ProblemSymptomsTable(tables.Table):
	id = tables.Column(linkify=True)
	symptom = tables.Column(linkify=True)
	class Meta:
		model = ProblemSymptom
		template_name = "django_tables2/bootstrap-responsive.html"
		
