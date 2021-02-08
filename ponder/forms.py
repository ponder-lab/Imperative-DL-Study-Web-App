#-*- coding: utf-8 -*-
from django import forms
from ponder.models import UserProfileInfo, Categorizations
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username','password','email')

class CategorizationForm(forms.ModelForm):
	'''
	sha = forms.CharField(label='sha', max_length=40)
	is_func_fix = forms.IntegerField(label='is_func_fix')
	func_fix_comment = forms.CharField(label='func_fix_comment', max_length=100)
	problem_category = forms.IntegerField(label='problem_category')
	problem_cause = forms.IntegerField(label='problem_cause')
	problem_symptom = forms.IntegerField(label='problem_symptom')
	problem_fix = forms.IntegerField(label='problem_fix')
	categorizer = forms.IntegerField(label='categorizer')
	bug_fix_id = forms.IntegerField(label='bug_fix_id')
	category_comment = forms.CharField(label='category_comment', max_length=140)
	cause_comment = forms.CharField(label='cause_comment', max_length=140)
	symptom_comment = forms.CharField(label='symptom_comment', max_length=140)
	fix_comment = forms.CharField(label='fix_comment', max_length=140)
	should_discuss = forms.IntegerField(label='sha')
	'''
	class Meta():
		model = Categorizations
		fields = ('sha', 'is_func_fix', 'func_fix_comment', 'problem_category',
			'category_comment','problem_cause','cause_comment',
			'cause_comment','problem_symptom', 'symptom_comment',
			'problem_fix', 'fix_comment', 'categorizer',
			'should_discuss', 'bug_fix')

class UserProfileInfoForm(forms.ModelForm):
	 class Meta():
		 model = UserProfileInfo
		 fields = ('portofolio_site',)