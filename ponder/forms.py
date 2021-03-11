#-*- coding: utf-8 -*-
from django import forms
from ponder.models import Categorizations, ProblemCategories, ProblemCauses, ProblemFixes, ProblemSymptoms, Commits,Categorizers
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from ponder.fields import CategoriesIssuesTextWidget

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username','password','email')
		
class CategorizationForm(forms.ModelForm):
	CHOICES = [('0', 'False'), ('1', 'True')]
	is_func_fix = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	should_discuss = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required= False)
	problem_category = forms.ModelChoiceField(queryset=ProblemCategories.objects.all(), required=False)
	problem_cause = forms.ModelChoiceField(queryset=ProblemCauses.objects.all(), required=False)
	problem_fix = forms.ModelChoiceField(queryset=ProblemFixes.objects.all(), required=False)
	problem_symptom = forms.ModelChoiceField(queryset=ProblemSymptoms.objects.all(), required=False)
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
		pc = kwargs.pop('problem_category', None)
		ps = kwargs.pop('problem_symptom', None)
		pf = kwargs.pop('problem_fix', None)
		pcause = kwargs.pop('problem_cause', None)
		super(CategorizationForm,self).__init__(*args,**kwargs)
		self.fields['problem_category'].widget = CategoriesIssuesTextWidget(data_list = pc, name = 'problem_category')
		self.fields['problem_cause'].widget = CategoriesIssuesTextWidget(data_list = pcause, name = 'problem_cause')
		self.fields['problem_fix'].widget = CategoriesIssuesTextWidget(data_list = pf, name = 'problem_fix')
		self.fields['problem_symptom'].widget = CategoriesIssuesTextWidget(data_list = ps, name = 'problem_symptom')

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
