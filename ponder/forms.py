#-*- coding: utf-8 -*-
from django import forms
from ponder.models import Categorizations, ProblemCategories, ProblemCauses, ProblemFixes, ProblemSymptoms, Commits
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username','password','email')

class CategorizationForm(forms.ModelForm):
	CHOICES = [('0', 'True'), ('1', 'False')]
	is_func_fix = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	class Meta():
		model = Categorizations
		fields = ('sha', 'is_func_fix', 'func_fix_comment', 'problem_category', 
			'category_comment','problem_cause','cause_comment',
			'problem_symptom', 'symptom_comment',
			'problem_fix', 'fix_comment', 'categorizer',
			'should_discuss')
		exclude = ('categorizer',)
	def __init__(self, user=None, rounds=None, **kwargs):
		super(CategorizationForm, self).__init__(**kwargs)
		if user and rounds:
			self.fields['sha'].queryset = models.Commits.objects.filter(rounds=rounds)
			self.fields['categorizer'].queryset = models.Categorizer.objects.filter(categorizer=user)


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
