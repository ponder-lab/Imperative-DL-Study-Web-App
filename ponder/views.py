import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django_filters import FilterSet
from django_filters.views import FilterView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django_tables2 import SingleTableView, SingleTableMixin

from ponder.forms import CategorizationForm, CategorizerForm
from .models import Categorization, User, BugFix, Categorizer, CommitDetail, Commit, ProblemCategory, ProblemCause, \
	ProblemFix, ProblemSymptom
from .tables import Categorizations_FilterTable, BugFixes_FilterTable, BugFixesTable, CommitDetailsTable, CommitsTable

class SHAFilter(FilterSet):
    class Meta:
        model = BugFix
        fields = {"sha" }

def index(request):
	user = request.user.username
	if request.user.pk in [1, 11, 14]:
		groups = ['Admin', 'Reconciler', 'Categorizer']
	else:
		groups = ['Categorizer']

	if 'role' in request.GET:
		selected_role = request.GET['role']
		gp = Group.objects.get(name=selected_role)
		request.user.groups.clear()
		request.user.groups.add(gp)
	if Categorizer.objects.values_list('id', flat=True).filter(user=user).exists():
		parts = ['Commits','Categorizations','Bug Fixes']
	else:
		parts = ['Commits','Bug Fixes']
	context = {'projects': parts, 'groups': groups}
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
@permission_required('ponder.view_bugfix', login_url='/forbidden/')
def categorizations_by_bugFixID(request):
	try:
		s = request.path_info
		s = s. replace('/bug_fixes/', '')
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
			if pb_category == None:
				pb_category = '-'
		except:
			pb_category = '—'
		try:
			pb_cause = obj.problem_cause
			if pb_cause == None:
				pb_cause = '-'
		except:
			pb_cause = '—'
		try:
			pb_symptom = obj.problem_symptom
			if pb_symptom == None:
				pb_symptom = '-'
		except:
			pb_symptom = '—'
		try:
			pb_fix = obj.problem_fix
			if pb_fix == None:
				pb_fix = '-'
		except:
			pb_fix = '—'

		context = {'table': table, 'id_value': id_value, 'sha': sha, 'is_func_fix': is_func_fix, 'project': project, \
				   'category_comment': activateLinks(obj.category_comment), 'cause_comment': activateLinks(obj.cause_comment), 'symptom_comment': activateLinks(obj.symptom_comment), 'fix_comment': activateLinks(obj.fix_comment), \
				   'pb_category': pb_category, 'pb_cause': pb_cause, 'pb_symptom': pb_symptom, 'pb_fix': pb_fix, 'should_discuss': should_discuss}
		return render(request, 'ponder/categorizations_by_BugFixID.html', context)
	except:
		return HttpResponse('<h1>Page Not Found </h1> <h2>Bug Fix does not exist</h2>', status=404)

@login_required
@permission_required('ponder.view_categorization', login_url='/forbidden/')
def categorizations_by_userID(request):
	user = request.user.username
	categorizerID = Categorizer.objects.values_list('id', flat=True).filter(user=user)
	try:
		name = list(categorizerID)[0]
	except:
		return HttpResponse('<h1>Page Not Found </h1> <h2>You have no access to this page</h2>', status=404)

	filter_by_round = Commit.objects.values_list('rounds', flat=True)
	filter_by_round = list(set(filter_by_round))
	filter_by_round.remove(None)

	if request.user.groups.all()[0].name == "Categorizer":
		categories = Categorization.objects.filter(categorizer=name)
		try:
			userID = request.GET['user']
		except:
			return HttpResponse('<h1>Page Not Found </h1> <h2>Categorizations cannot be found or viewed</h2>', status=404)

		if userID == str(request.user.id):
			try:
				r = request.GET['round']
				qs = Commit.objects.filter(rounds=r)
				query = []
				for p in qs:
					query += Categorization.objects.filter(sha=p.sha, categorizer=name)
				table = Categorizations_FilterTable(query)
			except:
				table = Categorizations_FilterTable(categories)
			table.order_by = "id"
			table.paginate(page=request.GET.get("page", 1), per_page=25)
			return render(request, 'ponder/categorizations_by_userID.html', {"table": table, "rounds": filter_by_round})
		else:
			return HttpResponse('<h1>Page Not Found </h1> <h2>Categorizations cannot be found or viewed</h2>', status=404)
	else:
		allCategorizations = Categorization.objects.all()
		user = User.objects.all()
		filter_by_user = list(set(user))
		try:
			r = request.GET['round']
			userID = request.GET['user']
			name = User.objects.filter(id=userID)
			name = str(list(set(name))[0])
			categorizer = Categorizer.objects.values_list(flat=True).filter(user=name)
			categorizerID = list(set(categorizer))[0]	
			qs = Commit.objects.filter(rounds=r)
			query = []
			for p in qs:
				query += Categorization.objects.filter(sha=p.sha, categorizer=categorizerID)
			table_by_round_userID = Categorizations_FilterTable(query)
		except:
			table_by_round_userID = Categorizations_FilterTable(allCategorizations)
		table_by_round_userID.order_by = "id"
		table_by_round_userID.paginate(page=request.GET.get("page", 1), per_page=25)
		try:
			r = request.GET['round']
			qs = Commit.objects.filter(rounds=r)
			query = []
			for p in qs:
				query += Categorization.objects.filter(sha=p.sha)
			table_by_round= Categorizations_FilterTable(query)
		except:
			table_by_round = Categorizations_FilterTable(allCategorizations)
		table_by_round.order_by = "id"
		table_by_round.paginate(page=request.GET.get("page", 1), per_page=25)
		try:
			userID = request.GET['user']
			name = User.objects.filter(id=userID)
			name = str(list(set(name))[0])
			categorizer = Categorizer.objects.values_list(flat=True).filter(user=name)
			categorizerID = list(set(categorizer))[0]
			categorizations = Categorization.objects.filter(categorizer=categorizerID)
			table_by_userID = Categorizations_FilterTable(categorizations)		
		except:
			table_by_userID = Categorizations_FilterTable(allCategorizations)		
		table_by_userID.order_by = "id"
		table_by_userID.paginate(page=request.GET.get("page", 1), per_page=25)
		return render(request, 'ponder/categorizations_by_userID.html', {"table_by_userID": table_by_userID, "table_by_round": table_by_round, "table_by_round_userID": table_by_round_userID, "rounds": filter_by_round, "users": filter_by_user})

def add_category(request, form):
	if not ProblemCategory.objects.filter(category=request.POST.get('category_text')).exists() and len(request.POST.get('category_text'))>=1 and any(c.isalnum() for c in request.POST.get('category_text')) and (request.POST.get('problem_category') == None or request.POST.get('problem_category') == ''):
		pb = ProblemCategory.objects.create(category=request.POST.get('category_text'),description=request.POST.get('category_description'))
		request.POST['problem_category'] = pb.id
		form.category_text = ''

	elif ProblemCategory.objects.filter(category=request.POST.get('category_text')).exists() and len(request.POST.get('category_text'))>=1 and (request.POST.get('problem_category') == None or request.POST.get('problem_category') == ''):
		request.POST['problem_category'] = str(ProblemCategory.objects.get(category=request.POST.get('category_text')).id)
		form.category_text = ''

	if not ProblemCause.objects.filter(cause=request.POST.get('cause_text')).exists() and len(request.POST.get('cause_text'))>=1 and any(c.isalnum() for c in request.POST.get('cause_text')) and (request.POST.get('problem_cause') == None or request.POST.get('problem_cause') == ''):
		pc = ProblemCause.objects.create(cause=request.POST.get('cause_text'), description=request.POST.get('cause_description'))
		request.POST['problem_cause'] = pc.id
		form.cause_text = ''

	elif ProblemCause.objects.filter(cause=request.POST.get('cause_text')).exists() and len(request.POST.get('cause_text'))>=1 and (request.POST.get('problem_cause') == None or request.POST.get('problem_cause') == ''):
		request.POST['problem_cause'] = str(ProblemCause.objects.get(cause=request.POST.get('cause_text')).id)
		form.cause_text = ''

	if not ProblemSymptom.objects.filter(symptom=request.POST.get('symptom_text')).exists() and len(request.POST.get('symptom_text'))>=1 and any(c.isalnum() for c in request.POST.get('symptom_text')) and (request.POST.get('problem_symptom') == None or request.POST.get('problem_symptom') == ''):
		ps = ProblemSymptom.objects.create(symptom=request.POST.get('symptom_text'), description=request.POST.get('symptom_description'))
		request.POST['problem_symptom'] = ps.id
		form.symptom_text = ''

	elif ProblemSymptom.objects.filter(symptom=request.POST.get('symptom_text')).exists() and len(request.POST.get('symptom_text'))>=1 and (request.POST.get('problem_symptom') == None or request.POST.get('problem_symptom') == ''):
		request.POST['problem_symptom'] = str(ProblemSymptom.objects.get(symptom=request.POST.get('symptom_text')).id)
		form.symptom_text = ''

	if not ProblemFix.objects.filter(fix=request.POST.get('fix_text')).exists() and len(request.POST.get('fix_text'))>=1 and any(c.isalnum() for c in request.POST.get('fix_text')) and (request.POST.get('problem_fix') == None or request.POST.get('problem_fix') == ''):
		pf = ProblemFix.objects.create(fix=request.POST.get('fix_text'), description=request.POST.get('fix_description'))
		request.POST['problem_fix'] = pf.id
		form.fix_text = ''

	elif ProblemFix.objects.filter(fix=request.POST.get('fix_text')).exists() and len(request.POST.get('fix_text'))>=1 and (request.POST.get('problem_fix') == None or request.POST.get('problem_fix') == ''):
		request.POST['problem_fix'] = str(ProblemFix.objects.get(fix=request.POST.get('fix_text')).id)
		form.fix_text = ''
@login_required
@permission_required(['ponder.add_categorization', 'ponder.add_problemcategory', 'ponder.add_problemcause'], login_url='/forbidden/')
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
		
		add_category(request, cat_form)
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
@permission_required('ponder.add_categorization', login_url='/forbidden/')
def success_categorization(request, pk):
	template = 'ponder/success_form.html'
	context = {'sha': pk}
	return render(request, template, context)

@login_required
@permission_required('ponder.change_categorization', login_url='/forbidden/')
def update_categorization(request):   
	form_update = Categorization.objects.get(id=request.GET['id'])
	sha = request.GET['commit']
	user = request.GET['user']
	sha_commits = Commit(sha=sha)
	project = Commit.objects.values('project').filter(sha=sha)[0]
	general_url = "https://github.com/"+str(project['project'])+"/search?q="+str(sha)
	commit_url = "https://github.com/"+str(project['project'])+"/commit/"+str(sha)
	cat_form = CategorizationForm('', '', '', '', '', '', '', '', sha=sha, user=user, instance=form_update)
	
	if request.method == 'POST':
		request.POST = request.POST.copy()
		cat_form = CategorizationForm(request.POST.get('category_text'), request.POST.get('category_description'), \
						request.POST.get('cause_text'), request.POST.get('cause_description'), \
						request.POST.get('fix_text'), request.POST.get('fix_description'), \
						request.POST.get('symptom_text'), request.POST.get('symptom_description'), \
						request.POST, sha=sha, user=user, instance=form_update)
		add_category(request, cat_form)
	
		if cat_form.is_valid():	
			cat_form.save()
			return HttpResponseRedirect('/categorizations?user=' + str(request.user.id))
		else:
			print(cat_form.errors.as_data())
	
	context = {'cat_form': cat_form,
				'sha': sha_commits,
				'general_url': general_url,
				'commit_url': commit_url}
	return render(request, 'ponder/categorizations.html', context)

@login_required
@permission_required('ponder.delete_categorization', login_url='/forbidden/')
def delete_categorization(request):
	item = Categorization.objects.get(id=request.GET['id'])
	item.delete()
	return HttpResponseRedirect('/categorizations?user=' + str(request.user.id))

@login_required
def permission_denied(request):
	return HttpResponse('<h1>Permission denied</h1> <h2>You have no permission to view or edit this content</h2>', status=403)

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				if user.groups.filter(name='Categorizer').exists() and not Categorizer.objects.filter(user=user).exists():
					return HttpResponseRedirect('/categorizers/new')
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'ponder/login.html', {})

@login_required
@permission_required(['ponder.add_categorization', 'ponder.add_problemcategory', 'ponder.add_problemcause'], login_url='/forbidden/')
def AddCategorizer(request):
	if request.method == 'POST':
		form = CategorizerForm(request.POST)
		if form.is_valid():
			categorizer = form.save(commit=False)
			# commit=False prevents Django from sending this to the database
			categorizer.user = request.user
			categorizer.save() #now this can be sent to the database
		return HttpResponseRedirect(reverse('index'))
	else:
		form = CategorizerForm()
		return render(request, 'ponder/categorizers.html', {"form": form})

@login_required
@permission_required('ponder.view_commit', login_url='/forbidden/')
def CommitsTableView(request):
	filter_by_round = Commit.objects.values_list('rounds', flat=True)
	filter_by_round = list(set(filter_by_round))
	commits = Commit.objects.all()

	try:
		r = request.GET['round']
		qs = Commit.objects.filter(rounds=r)
		query = []
		for p in qs:
			query += Commit.objects.filter(sha=p.sha)
		table = CommitsTable(query)
	except:
		table = CommitsTable(commits)
		
	table.order_by = "id"
	table.paginate(page=request.GET.get("page", 1), per_page=25)
	return render(request, 'ponder/commits_table.html', {"table": table, "rounds": filter_by_round})

class CommitDetailsTableView(LoginRequiredMixin, PermissionRequiredMixin, SingleTableView):
	login_url = 'ponder:user_login'
	permission_required = 'ponder.view_commitdetail'
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

class BugFixesTableView(LoginRequiredMixin, PermissionRequiredMixin, SingleTableMixin, FilterView):
	permission_required = 'ponder.view_bugfix'
	model = BugFix
	table_class = BugFixesTable
	filterset_class = SHAFilter
	template_name = 'ponder/bugfixes_table.html'
