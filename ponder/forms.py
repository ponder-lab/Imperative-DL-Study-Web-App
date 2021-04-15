#-*- coding: utf-8 -*-
from django import forms
from ponder.models import Categorization, ProblemCategory, ProblemCause, ProblemFix, ProblemSymptom, Commit,Categorizer
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from ponder.fields import CategoriesIssuesTextWidget
from bootstrap_modal_forms.forms import BSModalModelForm

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username','password','email')
		
class CategorizationForm(forms.ModelForm):
	problem_category = forms.ModelChoiceField(queryset=ProblemCategory.objects.all(), required=False)
	problem_cause = forms.ModelChoiceField(queryset=ProblemCause.objects.all(), required=False)
	problem_fix = forms.ModelChoiceField(queryset=ProblemFix.objects.all(), required=False)
	problem_symptom = forms.ModelChoiceField(queryset=ProblemSymptom.objects.all(), required=False)
	should_discuss = forms.BooleanField(required=False)

	class Meta():
		model = Categorization
		fields = ('is_func_fix', 'func_fix_comment', 'problem_category', 
			'category_comment','problem_cause','cause_comment',
			'problem_symptom', 'symptom_comment',
			'problem_fix', 'fix_comment',
			'should_discuss')

	def __init__(self,*args,**kwargs):
		sha = kwargs.pop('sha')
		user = kwargs.pop('user')
		super(CategorizationForm,self).__init__(*args,**kwargs)

class ProblemCategoryPopup(BSModalModelForm):
	category = forms.CharField(max_length=512,required=True)
	description = forms.CharField(max_length=512,required=False)
	class Meta:
		model = ProblemCategory
		fields = ['category','description']

class ProblemCausePopup(BSModalModelForm):
	cause = forms.CharField(max_length=512,required=True)
	description = forms.CharField(max_length=512,required=False)
	class Meta:
		model = ProblemCause
		fields = ['cause','description']

class ProblemSymptomPopup(BSModalModelForm):
	symptom = forms.CharField(max_length=512,required=True)
	class Meta:
		model = ProblemSymptom
		fields = ['symptom',]

class ProblemFixPopup(BSModalModelForm):
	fix = forms.CharField(max_length=512,required=True)
	class Meta:
		model = ProblemFix
		fields = ['fix',]

class ProblemCategoryForm(forms.ModelForm):
	class Meta(): 
		model = ProblemCategory
		fields = ('category','description')

class ProblemCausesForm(forms.ModelForm):
	class Meta(): 
		model = ProblemCause
		fields = ('cause','description')

class ProblemFixesForm(forms.ModelForm):
	class Meta(): 
		model = ProblemFix
		fields = ('fix',)

class ProblemSymptomsForm(forms.ModelForm):
	class Meta(): 
		model = ProblemSymptom
		fields = ('symptom',)

class RoundForm(forms.ModelForm):
	class Meta(): 
		model = Commit
		fields = ('rounds',)
