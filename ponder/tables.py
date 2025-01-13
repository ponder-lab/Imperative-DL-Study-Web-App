import re

import django_tables2 as tables
from django.utils.html import format_html

from .models import Categorization, BugFix, Categorizer, CommitDetail, Commit, Dataset, ProblemCategory, ProblemCause, \
	ProblemFix, ProblemSymptom


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
	sha = tables.Column(linkify=lambda record: record.get_sha(), attrs={"a": {"target": "_blank"}}, verbose_name='SHA')
	problem_category = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_category.description if record.problem_category != None else None}})
	problem_cause = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_cause.description if record.problem_cause != None else None}})
	problem_symptom = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_symptom.description if record.problem_symptom != None else None}})
	problem_fix = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_fix.description if record.problem_fix != None else None}})
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
	project = tables.Column(linkify=lambda record: record.get_project(), attrs={"a": {"target": "_blank"}})
	author = tables.Column(linkify=lambda record: record.email_author())
	sha = tables.Column(linkify=lambda record: record.get_commit(), attrs={"a": {"target": "_blank"}}, verbose_name='SHA')
	dataset = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.dataset.description}})
	go_to_details = tables.TemplateColumn('<a href=\"{% url \'ponder:commits_details\' record.id %}\">{{record.id}}</a>', verbose_name="ID")
	_ = tables.TemplateColumn('<a class="btn btn-info btn-sm" href=\"{% url \'ponder:categorizations_add\' %}?commit={{record.sha}}\">Add categorization</a>')

	class Meta:
		model = Commit
		exclude = ('author_email','id')
		template_name = "django_tables2/bootstrap-responsive.html"
		sequence = ('go_to_details','project', 'sha', 'author', 'commit_date', 'dataset', 'rounds', '_')

	def before_render(self, request):
		if not request.user.has_perm('ponder.add_categorization') or not request.user.has_perm('ponder.add_problemcategory') or not request.user.has_perm('ponder.add_problemcause'):
			self.columns.hide('_')

class Categorizations_FilterTable(tables.Table):
	sha = tables.Column(linkify=lambda record: record.get_sha(), attrs={"a": {"target": "_blank"}}, verbose_name='SHA')
	bug_fix = tables.Column(linkify=True)
	categorizer = tables.Column(linkify=lambda record: record.email_categorizer())
	problem_category = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_category.description if record.problem_category != None else None}})
	problem_cause = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_cause.description if record.problem_cause != None else None}})
	problem_symptom = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_symptom.description if record.problem_symptom != None else None}})
	problem_fix = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_fix.description if record.problem_fix != None else None}})
	Round = tables.TemplateColumn('{{}}')
	_ = tables.TemplateColumn('<a href=\"{% url \'ponder:update_categorization\'%}?user={{user.id}}&id={{record.id}}&commit={{record.sha}}\" class="btn btn-info btn-sm">Update</a>')
	__ = tables.TemplateColumn('<a href=\"{% url \'ponder:delete_categorization\'%}?user={{user.id}}&id={{record.id}}\" onclick=\"return confirm(\'Are you sure you want to delete this categorization?\');\" class="btn btn-danger btn-sm">Delete</a>')
	class Meta:
		model = Categorization
		template_name = "django_tables2/bootstrap-responsive.html"
		
	def before_render(self, request):
		if not request.user.has_perm('ponder.change_categorization'):
			self.columns.hide('_')

		if not request.user.has_perm('ponder.delete_categorization'):	
			self.columns.hide('__')
		
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
	sha = tables.Column(linkify=lambda record: record.get_sha(), attrs={"a": {"target": "_blank"}}, verbose_name='SHA')
	categorizer = tables.Column(linkify=lambda record: record.email_categorizer())
	problem_category = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_category.description if record.problem_category != None else None}})
	problem_cause = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_cause.description if record.problem_cause != None else None}})
	problem_symptom = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_symptom.description if record.problem_symptom != None else None}})
	problem_fix = tables.Column(attrs={'td': {"class": "tooltiptext", "title": lambda record: record.problem_fix.description if record.problem_fix != None else None}})
	class Meta:
		model = Categorization
		exclude = ('bug_fix',)
		template_name = "django_tables2/bootstrap-responsive.html"

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
		
