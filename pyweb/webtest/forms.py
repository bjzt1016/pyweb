#coding:utf-8
from django import forms

class TaskbotForm(forms.Form):
	python_code = forms.CharField(widget=forms.HiddenInput(attrs={'rows': '10', 'id': 'content'}), label='编辑代码', max_length=5000)

	# def  clean_python_code(self):
	# 	temp_python_code = self.cleaned_data.get('python_code') #unicode
	# 	if not temp_python_code:
	# 		raise forms.ValidationError('不能出现为空!')

	# 	return temp_python_code ###return at list