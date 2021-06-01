#-*- coding: utf-8 -*-
from django import forms
from ponder.models import Categorization, ProblemCategory, ProblemCause, ProblemFix, ProblemSymptom, Commit,Categorizer
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username','password','email')
		
class SelectWithData(forms.Select):
	option_data = {}

	def __init__(self, attrs=None, choices=(), option_data={}):
		super(SelectWithData, self).__init__(attrs, choices)
		self.option_data = option_data

	def get_context(self, name, value, attrs):
		context = super(SelectWithData, self).get_context(name, value, attrs)
		for optgroup in context['widget'].get('optgroups', []):
			for option in optgroup[1]:
				if (option['value'] != '' and option['name'] == 'problem_cause'):
					option['attrs']['title'] = ProblemCause.objects.values().get(id=option['value'].value)['description']
				if (option['value'] != '' and option['name'] == 'problem_category'):
					option['attrs']['title'] = ProblemCategory.objects.values().get(id=option['value'].value)['description']
				if (option['value'] != '' and option['name'] == 'problem_symptom'):
					option['attrs']['title'] = ProblemSymptom.objects.values().get(id=option['value'].value)['description']
				if (option['value'] != '' and option['name'] == 'problem_fix'):
					option['attrs']['title'] = ProblemFix.objects.values().get(id=option['value'].value)['description']
		return context

# TODO: Form validation should happen inside the form class. See https://bit.ly/3uHBXbA, https://bit.ly/34CxnAH, and https://bit.ly/2SHKsWJ.
class CategorizationForm(forms.ModelForm):
	problem_category = forms.ModelChoiceField(queryset=ProblemCategory.objects.all(), widget = SelectWithData(), required=False)
	problem_cause = forms.ModelChoiceField(queryset=ProblemCause.objects.all(), widget = SelectWithData(),required=False)
	problem_fix = forms.ModelChoiceField(queryset=ProblemFix.objects.all(), widget = SelectWithData(), required=False)
	problem_symptom = forms.ModelChoiceField(queryset=ProblemSymptom.objects.all(), widget = SelectWithData(), required=False)
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
