#-*- coding: utf-8 -*-
from django import forms
from ponder.models import Categorizations, ProblemCategories, ProblemCauses, ProblemFixes, ProblemSymptoms, Commits,Categorizers
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session



class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username','password','email')
		
class CategorizationForm(forms.ModelForm):
	CHOICES = [('0', 'False'), ('1', 'True')]
	is_func_fix = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	should_discuss = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=False)
	problem_category = forms.CharField(max_length=512,required=False)
	problem_cause = forms.CharField(max_length=512,required=False)
	problem_fix = forms.CharField(max_length=512,required=False)
	problem_symptom = forms.CharField(max_length=512,required=False)
	class Meta():
		model = Categorizations
		fields = ('is_func_fix', 'func_fix_comment', 'problem_category', 
			'category_comment','problem_cause','cause_comment',
			'problem_symptom', 'symptom_comment',
			'problem_fix', 'fix_comment',
			'should_discuss')
	def __init__(self,*args,**kwargs):
		sha = kwargs.pop('sha')
		user = kwargs.pop('user')
		super(CategorizationForm,self).__init__(*args,**kwargs)

class ProblemCategoryForm(forms.ModelForm):
	class Meta(): 
		model = ProblemCategories
		fields = ('category','description')

class ProblemCausesForm(forms.ModelForm):
	class Meta(): 
		model = ProblemCauses
		fields = ('cause','description')

class ProblemFixesForm(forms.ModelForm):
	class Meta(): 
		model = ProblemFixes
		fields = ('fix',)

class ProblemSymptomsForm(forms.ModelForm):
	class Meta(): 
		model = ProblemSymptoms
		fields = ('symptom',)

class RoundForm(forms.ModelForm):
	class Meta(): 
		model = Commits
		fields = ('rounds',)
