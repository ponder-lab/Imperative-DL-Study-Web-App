from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Categorization, User, BugFix, Categorizer, CommitDetail, Commit, Dataset, ProblemCategory, ProblemCause, ProblemFix, ProblemSymptom
from django.http import Http404
from ponder.forms import UserForm, CategorizationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import Categorizations_FilterTable, BugFixes_FilterTable, CategorizationsTable, BugFixesTable, CategorizersTable, CommitDetailsTable, CommitsTable, DatasetsTable, ProblemCategoriesTable, ProblemCausesTable, ProblemFixesTable, ProblemSymptomsTable
from .filters import RoundFilter
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django_tables2 import views
from django_tables2 import MultiTableMixin
from django_tables2 import RequestConfig
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from bootstrap_modal_forms.generic import BSModalCreateView
from django.db.models import Max
from django.utils.html import format_html
import re
from django.core.exceptions import ValidationError


def index(request):
	user = request.user.username
	if Categorizer.objects.values_list('id', flat=True).filter(user=user).exists():
		parts = ['Commits','Categorizations','Bug Fixes']
	else:
		parts = ['Commits','Bug Fixes']
	context = {'projects': parts}
	return render(request, 'ponder/index.html', context)

@login_required
def special(request):
	return HttpResponse("You are logged in")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def activateLinks(text):
        if text == None:
                text = '-'
        pattern = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
        result = ""
        idx = 0
        for match in pattern.finditer(text):
                start, end = match.start(0), match.end(0)
                result = format_html("{}{}<a href='{}'>{}</a>", result, text[idx:start], text[start:end], text[start:end])
                idx = end
        result = format_html("{}{}", result, text[idx:])
        return result

@login_required
def categorizations_by_bugFixID(request):
	try:
		s = request.path_info
		s = s. replace('/ponder/bug_fixes/', '')
		s = s. replace('/', '')
		id_value = int(s)
		id_qs = BugFix.objects.filter(id=id_value)
		sha = id_qs.values_list('sha', flat=True).get(pk=id_value)
		fix_details = Categorization.objects.filter(bug_fix=id_value)
		table = BugFixes_FilterTable(fix_details)
		table.paginate(page=request.GET.get("page", 1), per_page=25)
		obj = id_qs[0]
		is_func_fix = obj.is_func_fix
		should_discuss = obj.should_discuss
		project = Commit.objects.values('project').filter(sha=sha)[0]
		project = str(project['project'])
		if is_func_fix == False:
			is_func_fix = '✘'
		else:
			is_func_fix = '✔'     

		if should_discuss == False:
			should_discuss = '✘'
		else:
			should_discuss = '✔'
		try:
			pb_category = obj.problem_category
		except:
			pb_category = '—'
		try:
			pb_cause = obj.problem_cause
		except:
			pb_cause = '—'
		try:
			pb_symptom = obj.problem_symptom
		except:
			pb_symptom = '—'
		try:
			pb_fix = obj.problem_fix
		except:
			pb_fix = '—'
			
		context = {'table': table, 'id_value': id_value, 'sha': sha, 'is_func_fix': is_func_fix, 'project': project, \
				   'category_comment': activateLinks(obj.category_comment), 'cause_comment': activateLinks(obj.cause_comment), 'symptom_comment': activateLinks(obj.symptom_comment), 'fix_comment': activateLinks(obj.fix_comment), \
				   'pb_category': pb_category, 'pb_cause': pb_cause, 'pb_symptom': pb_symptom, 'pb_fix': pb_fix, 'should_discuss': should_discuss}
		return render(request, 'ponder/categorizations_by_BugFixID.html', context)
	except:
		return HttpResponse('<h1>Page Not Found </h1> <h2>Bug Fix does not exist</h2>', status=404)

@login_required
def categorizations_by_userID(request):
	user = request.user.username
	categorizerID = Categorizer.objects.values_list('id', flat=True).filter(user=user)
	try:
		name = list(categorizerID)[0]
	except:
		return HttpResponse('<h1>Page Not Found </h1> <h2>You have no access to this page</h2>', status=404)	
	categories = Categorization.objects.filter(categorizer=name)
	rounds = request.GET.get('rounds', '')
	if rounds.isnumeric():
		qs = Commit.objects.filter(rounds=rounds)
		categories = []
		for p in qs:
			categories += Categorization.objects.filter(sha=p.sha, categorizer=name)
	elif rounds != '':
		categories = []
	maxRound = Commit.objects.aggregate(Max('rounds'))['rounds__max']
	listOfRounds = range(1, maxRound + 1)
	table = Categorizations_FilterTable(categories)
	table.order_by = "id"
	table.paginate(page=request.GET.get("page", 1), per_page=25)
	userID = request.GET['user']
	if userID == str(request.user.id):
		return render(request, 'ponder/categorizations_by_userID.html', {"table":table, "listOfRounds":listOfRounds})
	else:
		return HttpResponse('<h1>Page Not Found </h1> <h2>Categorizations cannot be found or viewed</h2>', status=404)

@login_required
def AddCategorization(request):
	param_sha = request.GET.get('commit', '')
	sha_commits = Commit(sha=param_sha)
	project = Commit.objects.values('project').filter(sha=param_sha)[0]
	general_url = "https://github.com/"+str(project['project'])+"/search?q="+str(sha_commits)
	commit_url = "https://github.com/"+str(project['project'])+"/commit/"+str(sha_commits)

	if request.method == 'POST':
		request.POST = request.POST.copy()
	
		cat_form = CategorizationForm(request.POST.get('category_text'), request.POST.get('category_description'), \
									  request.POST.get('cause_text'), request.POST.get('cause_description'), \
									  request.POST.get('fix_text'), request.POST.get('fix_description'), \
									  request.POST.get('symptom_text'), request.POST.get('symptom_description'), \
									  request.POST, sha=sha_commits, user=request.user)	
		
		if not ProblemCategory.objects.filter(category=request.POST.get('category_text')).exists() and len(request.POST.get('category_text'))>=1 and (request.POST.get('problem_category') == None or request.POST.get('problem_category') == ''):
			pb = ProblemCategory.objects.create(category=request.POST.get('category_text'),description=request.POST.get('category_description'))
			request.POST['problem_category'] = pb.id
			cat_form.category_text = ''

		elif ProblemCategory.objects.filter(category=request.POST.get('category_text')).exists() and len(request.POST.get('category_text'))>=1 and (request.POST.get('problem_category') == None or request.POST.get('problem_category') == ''):
			request.POST['problem_category'] = str(ProblemCategory.objects.get(category=request.POST.get('category_text')).id)
			cat_form.category_text = ''

		if not ProblemCause.objects.filter(cause=request.POST.get('cause_text')).exists() and len(request.POST.get('cause_text'))>=1 and (request.POST.get('problem_cause') == None or request.POST.get('problem_cause') == ''):
			pc = ProblemCause.objects.create(cause=request.POST.get('cause_text'), description=request.POST.get('cause_description'))
			request.POST['problem_cause'] = pc.id
			cat_form.cause_text = ''

		elif ProblemCause.objects.filter(cause=request.POST.get('cause_text')).exists() and len(request.POST.get('cause_text'))>=1 and (request.POST.get('problem_cause') == None or request.POST.get('problem_cause') == ''):
			request.POST['problem_cause'] = str(ProblemCause.objects.get(cause=request.POST.get('cause_text')).id)
			cat_form.cause_text = ''

		if not ProblemSymptom.objects.filter(symptom=request.POST.get('symptom_text')).exists() and len(request.POST.get('symptom_text'))>=1 and (request.POST.get('problem_symptom') == None or request.POST.get('problem_symptom') == ''):
			ps = ProblemSymptom.objects.create(symptom=request.POST.get('symptom_text'), description=request.POST.get('symptom_description'))
			request.POST['problem_symptom'] = ps.id
			cat_form.symptom_text = ''

		elif ProblemSymptom.objects.filter(symptom=request.POST.get('symptom_text')).exists() and len(request.POST.get('symptom_text'))>=1 and (request.POST.get('problem_symptom') == None or request.POST.get('problem_symptom') == ''):
			request.POST['problem_symptom'] = str(ProblemSymptom.objects.get(symptom=request.POST.get('symptom_text')).id)
			cat_form.symptom_text = ''

		if not ProblemFix.objects.filter(fix=request.POST.get('fix_text')).exists() and len(request.POST.get('fix_text'))>=1 and (request.POST.get('problem_fix') == None or request.POST.get('problem_fix') == ''):
			pf = ProblemFix.objects.create(fix=request.POST.get('fix_text'), description=request.POST.get('fix_description'))
			request.POST['problem_fix'] = pf.id
			cat_form.fix_text = ''

		elif ProblemFix.objects.filter(fix=request.POST.get('fix_text')).exists() and len(request.POST.get('fix_text'))>=1 and (request.POST.get('problem_fix') == None or request.POST.get('problem_fix') == ''):
			request.POST['problem_fix'] = str(ProblemFix.objects.get(fix=request.POST.get('fix_text')).id)
			cat_form.fix_text = ''

		if cat_form.is_valid(): 
			categorization = cat_form.save(commit=False)
			username = User.objects.values('username').filter(id=request.user.id)[0]
			categorization.categorizer = Categorizer.objects.get(user = username['username'])

			# At this point, we have a good form submission. Let's save the categorization.
			categorization.sha = sha_commits
			categorization.save()
			
			# Render the succcess message.
			return HttpResponseRedirect(reverse('ponder:success_categorization', kwargs={'pk': param_sha}))
		else: # otherwise, we have a problem.
			print(cat_form.errors.as_data())
					
	else: # It is not a POST.
		# We just create the form.
		cat_form = CategorizationForm(request.POST.get('category_text'), request.POST.get('category_description'), \
									  request.POST.get('cause_text'), request.POST.get('cause_description'), \
									  request.POST.get('fix_text'), request.POST.get('fix_description'), \
									  request.POST.get('symptom_text'), request.POST.get('symptom_description'), \
									  request.POST, sha=sha_commits, user=request.user)

	context = {
		'cat_form': cat_form,
		'sha': sha_commits,
		'general_url': general_url,
		'commit_url': commit_url
		}

	# Here, we render the form.
	return render(request,'ponder/categorizations.html',context)

@login_required
def success_categorization(request, pk):
	template = 'ponder/success_form.html'
	context = {'sha': pk}
	return render(request, template, context)

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
								login(request,user)
								return HttpResponseRedirect(reverse('index'))
			else:
								return HttpResponse("Your account was inactive.")
		else:
						print("Someone tried to login and failed.")
						print("They used username: {} and password: {}".format(username,password))
						return HttpResponse("Invalid login details given")
	else:
		return render(request, 'ponder/login.html', {})

class CommitsTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
	login_url = 'ponder:user_login'
	model = Commit
	table_class = CommitsTable
	template_name = 'ponder/commits_table.html'
	filterset_class = RoundFilter

class CommitDetailsTableView(LoginRequiredMixin, SingleTableView):
	login_url = 'ponder:user_login'
	model = CommitDetail
	table_class = CommitDetailsTable
	template_name = 'ponder/commit_details_table.html'

	def get_queryset(self):
		c = Commit.objects.values('sha').filter(id=self.kwargs['pk'])[0]
		return CommitDetail.objects.filter(sha=c['sha'])
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sha'] = Commit.objects.values('sha').filter(id=self.kwargs['pk'])[0]['sha']
		return context

class BugFixesTableView(LoginRequiredMixin, SingleTableView):
	model = BugFix
	table_class = BugFixesTable
	template_name = 'ponder/bugfixes_table.html'
