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
	rounds_options = list(Commits.objects.order_by().values_list('rounds',flat=True).distinct())
	CHOICES = [('0', 'True'), ('1', 'False')]
	is_func_fix = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	rounds = forms.ChoiceField(choices=[(x, x) for x in rounds_options])

	class Meta():
		model = Categorizations
		fields = ('rounds', 'sha', 'is_func_fix', 'func_fix_comment', 'problem_category', 
			'category_comment','problem_cause','cause_comment',
			'problem_symptom', 'symptom_comment',
			'problem_fix', 'fix_comment', 'categorizer',
			'should_discuss')
		exclude = ('categorizer',)
	def __init__(self, *args, **kwargs):
		super(CategorizationForm, self).__init__(*args,**kwargs)
		self.fields['sha'].queryset = Commits.objects.none()
		#self.fields['categorizer'].queryset = Categorizers.objects.filter(categorizer=request.user)


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
