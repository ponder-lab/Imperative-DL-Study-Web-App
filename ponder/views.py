from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Categorization, User, BugFix, Categorizer, CommitDetail, Commit, Dataset, ProblemCategory, ProblemCause, ProblemFix, ProblemSymptom
from django.http import Http404
from ponder.forms import UserForm, CategorizationForm, ProblemCategoryForm, ProblemCausesForm, ProblemFixesForm, ProblemSymptomsForm, RoundForm
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
from django_tables2   import RequestConfig
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

def index(request):
	parts = ['Commits','Categorizations','Bug Fixes']
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
		#'values_pcat': ProblemCategory.objects.all(),
		#'values_pf': ProblemFix.objects.all(),
		#'values_pcause': ProblemCause.objects.all(),
		#'values_ps': ProblemSymptom.objects.all(),
		}
	return render(request, 'ponder/categorizations_problem.html', context)


@login_required
def id(request):
	try:
		s = request.path_info
		s = s. replace('/ponder/bug_fixes/', '')
		s = s. replace('/', '')
		id_value = int(s)
		id_qs = BugFix.objects.filter(id=id_value)
		sha = id_qs.values_list('sha', flat=True).get(pk=id_value)
		fix_details = Categorization.objects.filter(sha=sha)
		table = BugFixes_FilterTable(fix_details)
		return render(request, 'ponder/categorizations_filter1.html',{'table': table})
	except:
                return HttpResponse('<h1>Page Not Found </h1> <h2>Bug Fix does not exist</h2>', status=404)

@login_required
def search(request):
	user = request.user.username
	print(user)
	categorizerID = Categorizer.objects.values_list('id', flat=True).filter(user=user)
	print(categorizerID)
	name = list(categorizerID)[0]
	categories = Categorization.objects.filter(categorizer=name)
	table = Categorizations_FilterTable(categories)
	userID = request.GET['user']
	if userID == str(request.user.id):
		return render(request, 'ponder/categorizations_filter2.html', {"table":table})

	else:
		return HttpResponse('<h1>Page Not Found </h1> <h2>Categorizations cannot be found or viewed</h2>', status=404)

@login_required
def categorizations(request,pk):
	sha_commits=Commit(sha=pk)
	project = Commit.objects.values('project').filter(sha=pk)[0]
	general_url = "https://github.com/"+str(project['project'])+"/search?q="+str(sha_commits)
	commit_url = "https://github.com/"+str(project['project'])+"/commit/"+str(sha_commits)
	categories = []
	fixes = []
	causes = []
	symptoms =[]
	for i in range(len(ProblemCategory.objects.values('category').distinct())):
		c = ProblemCategory.objects.values('category').distinct()[i]
		if(c['category'] != 'None'): 
			categories.append(c['category'])
	for i in range(len(ProblemFix.objects.values('fix').distinct())):
		c = ProblemFix.objects.values('fix').distinct()[i]
		if(c['fix'] != 'None'): 
			fixes.append(c['fix'])
	for i in range(len(ProblemCause.objects.values('cause').distinct())):
		c = ProblemCause.objects.values('cause').distinct()[i]
		if(c['cause'] != 'None'): 
			causes.append(c['cause'])
	for i in range(len(ProblemSymptom.objects.values('symptom').distinct())):
		c = ProblemSymptom.objects.values('symptom').distinct()[i]
		if(c['symptom'] != 'None'): 
			symptoms.append(c['symptom'])
	if request.method == 'POST':
		cat_form = CategorizationForm(request.POST,sha=sha_commits, user = request.user, problem_cause = causes, problem_fix = fixes, problem_category = categories, problem_symptom = symptoms)
		if request.POST.get('is_func_fix') == '1':
			cat_form.fields['problem_category'].required = True
			if(request.POST.get('problem_category') != 'Unknown' and request.POST.get('problem_category')!='Test' and request.POST.get('problem_category') != 'Other'):
				cat_form.fields['problem_symptom'].required = True
				cat_form.fields['problem_fix'].required = True 
				cat_form.fields['problem_cause'].required = True 
			cat_form.fields['should_discuss'].required = True 

		if cat_form.is_valid():
			categorization = cat_form.save(commit=False)
			username = User.objects.values('username').filter(id=request.user.id)[0]
			username = Categorizer.objects.values('id').filter(user=username['username'])[0]
			categorization.categorizer = username['id']
			if not ProblemCategory.objects.filter(category=cat_form.cleaned_data['problem_category']).exists():
				ProblemCategory.objects.create(category=cat_form.cleaned_data['problem_category'])

			if not cat_form.cleaned_data['problem_category']: 
				categorization.problem_category = None
			else:
				problem_category = ProblemCategory.objects.values('id').filter(category=cat_form.cleaned_data['problem_category'])[0]
				categorization.problem_category = problem_category['id'] 

			if not ProblemCause.objects.filter(cause=cat_form.cleaned_data['problem_cause']).exists() and len(cat_form.cleaned_data['problem_cause'])>=1:
				ProblemCause.objects.create(cause=cat_form.cleaned_data['problem_cause'])

			if not cat_form.cleaned_data['problem_cause']: 
				categorization.problem_cause = None
			else:
				problem_cause = ProblemCause.objects.values('id').filter(cause=cat_form.cleaned_data['problem_cause'])[0]
				categorization.problem_cause = problem_cause['id']

			if not ProblemFix.objects.filter(fix=cat_form.cleaned_data['problem_fix']).exists() and len(cat_form.cleaned_data['problem_fix'])>=1:
				ProblemFix.objects.create(fix=cat_form.cleaned_data['problem_fix'])

			if not cat_form.cleaned_data['problem_fix']: 
				categorization.problem_fix = None
			else:
				problem_fix = ProblemFix.objects.values('id').filter(fix=cat_form.cleaned_data['problem_fix'])[0]
				categorization.problem_fix = problem_fix['id']

			if not ProblemSymptom.objects.filter(symptom=cat_form.cleaned_data['problem_symptom']).exists() and len(cat_form.cleaned_data['problem_symptom'])>=1:
				ProblemSymptom.objects.create(symptom=cat_form.cleaned_data['problem_symptom'])

			if not cat_form.cleaned_data['problem_symptom']: 
				categorization.problem_symptom = None
			else: 
				problem_symptom = ProblemSymptom.objects.values('id').filter(symptom=cat_form.cleaned_data['problem_symptom'])[0]
				categorization.problem_symptom = problem_symptom['id']

			if cat_form.cleaned_data['should_discuss']=='':
				categorization.should_discuss = None

			categorization.sha=sha_commits
			categorization.save()
			return HttpResponseRedirect(reverse('ponder:success_categorization'))
		else: 
			print(cat_form.errors)
	else:
		cat_form = CategorizationForm(request.POST,sha=sha_commits, user = request.user, problem_cause = causes, problem_fix = fixes, problem_category = categories, problem_symptom = symptoms)
	context = {
		'cat_form': cat_form,
		'sha': sha_commits,
		'general_url': general_url,
		'commit_url': commit_url
		}
	return render(request,'ponder/categorizations.html',context)

def success_categorization(request):
	template = 'ponder/success_form.html'
	context = {}
	return render(request, template, context)
"""
class CategorizationsCreateView(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	model = Categorization
	form_class = CategorizationForm
	sucess_url = reverse_lazy('categorization_changelist')

class CategorizationsListView(ListView):
	model = Categorization
	context_object_name = 'categorizations'

def load_shas(request):
	rounds = request.GET.get('rounds')
	commits = Commit.objects.filter(rounds=rounds)
	return render(request, 'ponder/shas_options.html', {'commits': commits})
"""

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

class BugFixesTableView(LoginRequiredMixin, SingleTableView):
    model = BugFix
    table_class = BugFixesTable
    template_name = 'ponder/bugfixes_table.html' 
	
"""
class CategorizationsListView(SingleTableView):
    model = Categorization
    table_class = CategorizationsTable
    template_name = 'ponder/categorizations_table.html' 

class CategorizersListView(SingleTableView):
    model = Categorizer
    table_class = CategorizersTable
    template_name = 'ponder/categorizers_table.html'

class CommitDetailsListView(SingleTableView):
    model = CommitDetail
    table_class = CommitDetailsTable
    template_name = 'ponder/commitdetails_table.html'

class CommitsListView(SingleTableView):
    model = Commit
    table_class = CommitsTable
    template_name = 'ponder/commits_table.html'

class DatasetsListView(SingleTableView):
    model = Dataset
    table_class = DatasetsTable
    template_name = 'ponder/datasets_table.html'

class ProblemCategoriesListView(SingleTableView):
    model = ProblemCategory
    table_class = ProblemCategoriesTable
    template_name = 'ponder/problemcategories_table.html'

class ProblemCausesListView(SingleTableView):
    model = ProblemCause
    table_class = ProblemCausesTable
    template_name = 'ponder/problemcauses_table.html' 

class ProblemFixesListView(SingleTableView):
    model = ProblemFix
    table_class = ProblemFixesTable
    template_name = 'ponder/problemfixes_table.html'

class ProblemSymptomsListView(SingleTableView):
    model = ProblemSymptom
    table_class = ProblemSymptomsTable
    template_name = 'ponder/problemsymptoms_table.html' 
    
"""
