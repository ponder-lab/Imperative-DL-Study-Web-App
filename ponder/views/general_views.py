import re
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from ponder.models import Categorizer, ProblemCategory, ProblemCause, ProblemSymptom, ProblemFix
from ponder.forms import CategorizerForm

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

def activateLinks(text):
    if text == None:
        text = '-'
    pattern = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
    result = ""
    idx = 0
    for match in pattern.finditer(text):
        start, end = match.start(0), match.end

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
