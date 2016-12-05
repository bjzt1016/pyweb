#coding:utf-8
import subprocess
import os
import codecs

from django.shortcuts import render
from .forms import TaskbotForm
from django.http import HttpResponse


# Create your views here.
def home(request):
	return HttpResponse('test url: http://127.0.0.1:8000/submit/;最多返回5000个字符')

def submit_code(request):
	form = TaskbotForm(request.POST or None)

	if form.is_valid():
		if request.method == 'POST':
			python_code = form.cleaned_data.get("python_code")
			temp_file = codecs.open('save_code.py', 'w', encoding='utf-8')
			temp_file.write(python_code)
			temp_file.close()

			# with open("save_code.py", 'w') as f:
			# 	f.write(python_code)

			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			PY_DIR = os.path.join(BASE_DIR, 'save_code.py')

			try:
				subprocess.check_call(["python", PY_DIR])
			except:
				return HttpResponse('error happened when running the code!')

			return_output = subprocess.check_output(["python", PY_DIR])
			# return HttpResponse(return_output)
			return render(request, 'temp.html', {"return_output": return_output})
	else:
		return render(request, 'submit_code_four.html', {"form": form,})
		# return render(request, 'submit_code_three.html', {"form": form,})
		# return render(request, 'submit_code_two.html', {"form": form,})
		# return render(request, 'submit_code_one.html', {"form": form,})
		# return render(request, 'submit_code.html', {"form": form,})