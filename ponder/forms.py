#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ponder.models import Categorization, ProblemCategory, ProblemCause, ProblemFix, ProblemSymptom, Categorizer


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

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

	def __init__(self,category_text,category_description,cause_text,cause_description,fix_text,fix_description,symptom_text,symptom_description,*args,**kwargs):
		sha = kwargs.pop('sha')
		user = kwargs.pop('user')
		self.category_text = category_text
		self.category_description = category_description
		self.cause_text = cause_text
		self.cause_description = cause_description
		self.fix_text = fix_text
		self.fix_description = fix_description
		self.symptom_text = symptom_text
		self.symptom_description = symptom_description
		super(CategorizationForm,self).__init__(*args,**kwargs)
	
	def clean_is_func_fix(self):
		if self['is_func_fix'].value() == False:
			if (self['problem_category'].value() != None and self['problem_category'].value() != '') or (self.category_text != '' and self.category_text != None and any(c.isalnum() for c in self.category_text)):
				raise ValidationError("This field should be checked. An existing problem category indicates a bug fix.")
			if (self['problem_cause'].value() != None and self['problem_cause'].value() != '') or (self.cause_text != '' and self.cause_text != None and any(c.isalnum() for c in self.cause_text)):
				raise ValidationError("This field should be checked. An existing problem cause indicates a bug fix.")
			if (self['problem_symptom'].value() != None and self['problem_symptom'].value() != '') or (self.symptom_text != '' and self.symptom_text != None and any(c.isalnum() for c in self.symptom_text)):
				raise ValidationError("This field should be checked. An existing problem symptom indicates a bug fix.")
			if (self['problem_fix'].value() != None and self['problem_fix'].value() != '') or (self.fix_text != '' and self.fix_text != None and any(c.isalnum() for c in self.fix_text)):
				raise ValidationError("This field should be checked. An existing problem fix indicates a bug fix.")
		return self.cleaned_data['is_func_fix']

	def clean_problem_category(self):
		if self['is_func_fix'].value() == True:
			if (self['problem_category'].value() == '' or self['problem_category'].value() == None) and len(self.category_text)>=1 and not any(c.isalnum() for c in self.category_text):
				raise ValidationError("Invalid characters. Please enter a valid category")
			elif (self['problem_category'].value() != None and self['problem_category'].value() != '') and (self.category_text != '' and self.category_text != None and any(c.isalnum() for c in self.category_text)):
				raise ValidationError("Choose only one option. Either select an existing problem category or enter a new one.")
			elif (self['problem_category'].value() == '' or self['problem_category'].value() == None) and (self.category_text == '' or self.category_text == None or not any(c.isalnum() for c in self.category_text)):
				raise ValidationError("This field is required. Select an existing problem category or enter a new one.")
		return self.cleaned_data['problem_category']

	def clean_problem_cause(self):
		if self['is_func_fix'].value() == True:
			if (self['problem_cause'].value() == '' or self['problem_cause'].value() == None) and len(self.cause_text)>=1 and not any(c.isalnum() for c in self.cause_text):
				raise ValidationError("Invalid characters. Please enter a valid category")
			elif (self['problem_cause'].value() != None and self['problem_cause'].value() != '') and (self.cause_text != '' and self.cause_text != None and any(c.isalnum() for c in self.cause_text)):
				raise ValidationError("Choose only one option. Either select an existing problem cause or enter a new one.")
			if self['problem_category'].value() == '1' or self['problem_category'].value() == '2' or self['problem_category'].value() == '5':
				pass
			elif (self['problem_category'].value() != None and self['problem_category'].value() != '') or (self.category_text != '' and self.category_text != None and any(c.isalnum() for c in self.category_text)):
				if (self['problem_cause'].value() == '' or self['problem_cause'].value() == None) and (self.cause_text == '' or self.cause_text == None or not any(c.isalnum() for c in self.cause_text)):
					raise ValidationError("This field is required. Select an existing problem cause or enter a new one.")		
		return self.cleaned_data['problem_cause']

	def clean_problem_symptom(self):
		if self['is_func_fix'].value() == True:
			if (self['problem_symptom'].value() == '' or self['problem_symptom'].value() == None) and len(self.symptom_text)>=1 and not any(c.isalnum() for c in self.symptom_text):
				raise ValidationError("Invalid characters. Please enter a valid category")
			elif (self['problem_symptom'].value() != None and self['problem_symptom'].value() != '') and (self.symptom_text != '' and self.symptom_text != None and any(c.isalnum() for c in self.symptom_text)):
				raise ValidationError("Choose only one option. Either select an existing problem symptom or enter a new one.")
			if self['problem_category'].value() == '1' or self['problem_category'].value() == '2' or self['problem_category'].value() == '5':
				pass
			elif (self['problem_category'].value() != None and self['problem_category'].value() != '') or (self.category_text != '' and self.category_text != None and any(c.isalnum() for c in self.category_text)):
				if (self['problem_symptom'].value() == '' or self['problem_symptom'].value() == None) and (self.symptom_text == '' or self.symptom_text == None or not any(c.isalnum() for c in self.symptom_text)):
					raise ValidationError("This field is required. Select an existing problem symptom or enter a new one.")
		return self.cleaned_data['problem_symptom']

	def clean_problem_fix(self):
		if self['is_func_fix'].value() == True:
			if (self['problem_fix'].value() == '' or self['problem_fix'].value() == None) and len(self.fix_text)>=1 and not any(c.isalnum() for c in self.fix_text):
				raise ValidationError("Invalid characters. Please enter a valid category")
			elif (self['problem_fix'].value() != None and self['problem_fix'].value() != '') and (self.fix_text != '' and self.fix_text != None and any(c.isalnum() for c in self.fix_text)):
				raise ValidationError("Choose only one option. Either select an existing problem fix or enter a new one.")
			if self['problem_category'].value() == '1' or self['problem_category'].value() == '2' or self['problem_category'].value() == '5':
				pass
			elif (self['problem_category'].value() != None and self['problem_category'].value() != '') or (self.category_text != '' and self.category_text != None and any(c.isalnum() for c in self.category_text)):
				if (self['problem_fix'].value() == '' or self['problem_fix'].value() == None) and (self.fix_text == '' or self.fix_text == None or not any(c.isalnum() for c in self.fix_text)):
					raise ValidationError("This field is required. Select an existing problem fix or enter a new one.")
		return self.cleaned_data['problem_fix']

	def clean(self):
		if self.errors.as_data() != {}:
			self.add_error(None, ("There was a problem submitting the form. Please enter valid input values."))

class CategorizerForm(forms.ModelForm):
	class Meta():
		model = Categorizer
		fields = ('name','initials')