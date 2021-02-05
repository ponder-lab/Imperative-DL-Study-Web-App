from django.shortcuts import render
from django.http import HttpResponse
from .models import Commits
from django.http import Http404
from .forms import LoginForm


def index(request,username):
	commits_list = Commits.objects.order_by('-commit_date')
	context = {'commits_list': commits_list}
	return render(request, 'ponder/index.html', context)

def detail(request, c_id):
	try:
		commit = Commits.objects.get(pk=c_id)
	except Commits.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'ponder/detail.html', {'commit': commit})

def categorization(request, c_id):
	response = "You're looking at categorization of commit %s."
	return HttpResponse(response % c_id)

def commit(request, c_id):
	return HttpResponse("You're looking at the commit %s." % c_id)

def login(request):
   username = "not logged in"
   
   if request.method == "POST":
      #Get the posted form
      MyLoginForm = LoginForm(request.POST)
      
      if MyLoginForm.is_valid():
         username = MyLoginForm.cleaned_data['username']
   else:
      MyLoginForm = Loginform()
		
   return render(request, 'ponder/index.html', {"username" : username})