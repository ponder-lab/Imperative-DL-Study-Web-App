from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Commits, Categorizations, User, BugFixes, Categorizers, CommitDetails, Commits, Datasets, ProblemCategories, ProblemCauses, ProblemFixes, ProblemSymptoms
from django.http import Http404
from ponder.forms import UserForm, CategorizationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import CategorizationsTable, BugFixesTable, CategorizersTable, CommitDetailsTable, CommitsTable, DatasetsTable, ProblemCategoriesTable, ProblemCausesTable, ProblemFixesTable, ProblemSymptomsTable
from django.apps import apps 
from django.contrib import admin 
from django.contrib.admin.sites import AlreadyRegistered 

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

def categorizations(request):
	if request.method == 'POST':
		cat_form = CategorizationForm(data=request.POST)
		if cat_form.is_valid():
			categorization = cat_form.save()
		else: 
			print(cat_form.errors)
	else:
		cat_form = CategorizationForm()
	return render(request,'ponder/categorizations.html', {'cat_form':cat_form})

def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			registered = True
		else:
			print(user_form.errors)
	else:
		user_form = UserForm()
	return render(request,'ponder/registration.html',
						  {'user_form':user_form,
						   'registered':registered})

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

class CategorizationsListView(SingleTableView):
    model = Categorizations
    table_class = CategorizationsTable
    template_name = 'ponder/categorizations_table.html'

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
