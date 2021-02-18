from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Commits, Categorizations, User, BugFixes, Categorizers, CommitDetails, Commits, Datasets, ProblemCategories, ProblemCauses, ProblemFixes, ProblemSymptoms
from django.http import Http404
from ponder.forms import UserForm, CategorizationForm, ProblemCategoryForm, ProblemCausesForm, ProblemFixesForm, ProblemSymptomsForm, RoundForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import CategorizationsTable, BugFixesTable, CategorizersTable, CommitDetailsTable, CommitsTable, DatasetsTable, ProblemCategoriesTable, ProblemCausesTable, ProblemFixesTable, ProblemSymptomsTable
from django.apps import apps 
from django.contrib import admin 
from django.contrib.admin.sites import AlreadyRegistered 
from django_tables2 import views
from django_tables2 import MultiTableMixin
from django_tables2   import RequestConfig
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

def index(request):
	parts = ['Categorizations','Reconciliation','Visualization of Data']
	context = {'projects': parts}
	return render(request, 'ponder/index.html', context)

@login_required
def special(request):
	return HttpResponse("You are logged in")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def problem_details(request):

	if request.method == 'POST':
		p_categoryF = ProblemCategoryForm(data=request.POST)
		p_fixF = ProblemFixesForm(data=request.POST)
		p_causeF = ProblemCausesForm(data=request.POST)
		p_symptomF = ProblemSymptomsForm(data=request.POST)

		if p_categoryF.is_valid() and p_fixF.is_valid() and p_causeF.is_valid() and p_symptomF.is_valid(): 
			p_category = p_categoryF.save()
			p_fix = p_fixF.save()
			p_cause = p_causeF.save()
			p_symptom = p_symptomF.save()
		else:
			print(p_categoryF.errors,p_fixF.errors, p_causeF.errors, p_symptomF.errors)
	else: 
		p_categoryF = ProblemCategoryForm()
		p_fixF = ProblemFixesForm()
		p_causeF = ProblemCausesForm()
		p_symptomF = ProblemSymptomsForm()

	context = {
		'p_category': p_categoryF,
		'p_fix': p_fixF,
		'p_cause': p_causeF,
		'p_symptom': p_symptomF,
		#'values_pcat': ProblemCategories.objects.all(),
		#'values_pf': ProblemFixes.objects.all(),
		#'values_pcause': ProblemCauses.objects.all(),
		#'values_ps': ProblemSymptoms.objects.all(),
		}
	return render(request, 'ponder/categorizations_problem.html', context)
"""
def categorizations(request):
	if request.method == 'POST':
		round_form = RoundForm(data=request.POST)
		if round_form.is_valid():
			current_round = round_form.cleaned_data['rounds']
			print(current_round)

		cat_form = CategorizationForm(rounds=current_round)
		if cat_form.is_valid():
			categorization = cat_form.save()
		else: 
			print(round_form.errors, cat_form.errors)
	else:
		round_form = RoundForm()
		cat_form = CategorizationForm()
	context = {
		'cat_form': cat_form,
		'round_form': round_form,
		}
	return render(request,'ponder/categorizations.html',context)
"""
class CategorizationsCreateView(CreateView):
	model = Categorizations
	form_class = CategorizationForm
	sucess_url = reverse_lazy('categorization_changelist')

class CategorizationsListView(ListView):
	model = Categorizations
	context_object_name = 'categorizations'

def load_shas(request):
	rounds = request.GET.get('rounds')
	commits = Commits.objects.filter(rounds=rounds)
	return render(request, 'ponder/shas_options.html', {'commits': commits})

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
"""
class CategorizationsListView(SingleTableView):
    model = Categorizations
    table_class = CategorizationsTable
    template_name = 'ponder/categorizations_table.html'
"""
class BugFixesListView(SingleTableView):
    model = BugFixes
    table_class = BugFixesTable
    template_name = 'ponder/bugfixes_table.html'  

class CategorizersListView(SingleTableView):
    model = Categorizers
    table_class = CategorizersTable
    template_name = 'ponder/categorizers_table.html'

class CommitDetailsListView(SingleTableView):
    model = CommitDetails
    table_class = CommitDetailsTable
    template_name = 'ponder/commitdetails_table.html'

class CommitsListView(SingleTableView):
    model = Commits
    table_class = CommitsTable
    template_name = 'ponder/commits_table.html'

class DatasetsListView(SingleTableView):
    model = Datasets
    table_class = DatasetsTable
    template_name = 'ponder/datasets_table.html'

class ProblemCategoriesListView(SingleTableView):
    model = ProblemCategories
    table_class = ProblemCategoriesTable
    template_name = 'ponder/problemcategories_table.html'

class ProblemCausesListView(SingleTableView):
    model = ProblemCauses
    table_class = ProblemCausesTable
    template_name = 'ponder/problemcauses_table.html' 

class ProblemFixesListView(SingleTableView):
    model = ProblemFixes
    table_class = ProblemFixesTable
    template_name = 'ponder/problemfixes_table.html'

class ProblemSymptomsListView(SingleTableView):
    model = ProblemSymptoms
    table_class = ProblemSymptomsTable
    template_name = 'ponder/problemsymptoms_table.html' 
