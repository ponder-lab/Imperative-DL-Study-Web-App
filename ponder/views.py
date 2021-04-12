from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Categorization, User, BugFix, Categorizer, CommitDetail, Commit, Dataset, ProblemCategory, ProblemCause, ProblemFix, ProblemSymptom
from django.http import Http404
from ponder.forms import UserForm, CategorizationForm, ProblemCategoryForm, ProblemCausesForm, ProblemFixesForm, ProblemSymptomsForm, RoundForm, ProblemCategoryPopup,ProblemCausePopup,ProblemFixPopup,ProblemSymptomPopup
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


@login_required
def categorizations_by_bugFixID(request):
	try:
		s = request.path_info
		s = s. replace('/ponder/bug_fixes/', '')
		s = s. replace('/', '')
		id_value = int(s)
		id_qs = BugFix.objects.filter(id=id_value)
		sha = id_qs.values_list('sha', flat=True).get(pk=id_value)
		fix_details = Categorization.objects.filter(sha=sha)
		fix_details = Categorization.objects.filter(bug_fix=id_value)
		table = BugFixes_FilterTable(fix_details)
		table.paginate(page=request.GET.get("page", 1), per_page=25)
		is_func_fix = BugFix.objects.values_list('is_func_fix', flat=True).filter(id=id_value)[0]
		project = Commit.objects.values('project').filter(sha=sha)[0]
        	project = str(project['project'])
		if is_func_fix == False:
			is_func_fix = '✘'
		else:
			is_func_fix = '✔'
		try:
			pb_category = BugFix.objects.prefetch_related('problem_category').filter(id=id_value)[0].problem_category
		except:
			pb_category = None
		return render(request, 'ponder/categorizations_filter1.html',{'table': table, 'id_value': id_value, 'sha': sha, 'is_func_fix': is_func_fix, 'problem_category': pb_category, 'project': project})
	except:
                return HttpResponse('<h1>Page Not Found </h1> <h2>Bug Fix does not exist</h2>', status=404)

@login_required
def categorizations_by_userID(request):
	user = request.user.username
	print(user)
	categorizerID = Categorizer.objects.values_list('id', flat=True).filter(user=user)
	print(categorizerID)
	name = list(categorizerID)[0]
	categories = Categorization.objects.filter(categorizer=name)
	table = Categorizations_FilterTable(categories)
	table.paginate(page=request.GET.get("page", 1), per_page=25)
	userID = request.GET['user']
	if userID == str(request.user.id):
		return render(request, 'ponder/categorizations_filter2.html', {"table":table})
	else:
		return HttpResponse('<h1>Page Not Found </h1> <h2>Categorizations cannot be found or viewed</h2>', status=404)

@login_required
def AddCategorization(request):
	param_sha = request.GET.get('commit', '')
	sha_commits=Commit(sha=param_sha)
	project = Commit.objects.values('project').filter(sha=param_sha)[0]
	general_url = "https://github.com/"+str(project['project'])+"/search?q="+str(sha_commits)
	commit_url = "https://github.com/"+str(project['project'])+"/commit/"+str(sha_commits)

	if request.method == 'POST':
		cat_form = CategorizationForm(request.POST,sha=sha_commits, user = request.user)
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
			categorization.categorizer = Categorizer.objects.get(user = username['username'])
			if cat_form.cleaned_data['should_discuss']=='':
				categorization.should_discuss = None
			categorization.sha=sha_commits
			categorization.save()
			return HttpResponseRedirect(reverse('ponder:success_categorization', kwargs={'pk': param_sha}))
		else: 
			print(cat_form.errors)
	else:
		cat_form = CategorizationForm(request.POST,sha=sha_commits, user = request.user)
	context = {
		'cat_form': cat_form,
		'sha': sha_commits,
		'general_url': general_url,
		'commit_url': commit_url
		}
	return render(request,'ponder/categorizations.html',context)


@login_required
def success_categorization(request, pk):
	template = 'ponder/success_form.html'
	context = {'sha': pk}
	return render(request, template, context)

class ProblemCategoryCreateView(BSModalCreateView):
	template_name = 'ponder/popup_prob_cat.html'
	form_class = ProblemCategoryPopup
	success_message = 'Success: Problem Category was created.'

	def get_success_url(self, **kwargs):
		obj = self.kwargs
		url =  reverse("ponder:categorizations_add")
		qs = 'commit=%s' % obj['pk']
		return '?'.join((url,qs))


class ProblemCauseCreateView(BSModalCreateView):
	template_name = 'ponder/popup_prob_cause.html'
	form_class = ProblemCausePopup
	success_message = 'Success: Problem Cause was created.'

	def get_success_url(self, **kwargs):
		obj = self.kwargs
		url =  reverse("ponder:categorizations_add")
		qs = 'commit=%s' % obj['pk']
		return '?'.join((url,qs))

class ProblemSymptomCreateView(BSModalCreateView):
	template_name = 'ponder/popup_prob_symptom.html'
	form_class = ProblemSymptomPopup
	success_message = 'Success: Problem Symptom was created.'

	def get_success_url(self, **kwargs):
		obj = self.kwargs
		url =  reverse("ponder:categorizations_add")
		qs = 'commit=%s' % obj['pk']
		return '?'.join((url,qs))

class ProblemFixCreateView(BSModalCreateView):
	template_name = 'ponder/popup_prob_fix.html'
	form_class = ProblemFixPopup
	success_message = 'Success: Problem Fix was created.'

	def get_success_url(self, **kwargs):
		obj = self.kwargs
		url =  reverse("ponder:categorizations_add")
		qs = 'commit=%s' % obj['pk']
		return '?'.join((url,qs))

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
