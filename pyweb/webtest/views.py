#coding:utf-8
import subprocess
import os
import codecs
import json

from django.shortcuts import render
from .forms import TaskbotForm
from django.http import HttpResponse


# Create your views here.
def home(request):
	# return HttpResponse('test url: http://127.0.0.1:8000/submit/;最多返回5000个字符')
	form = TaskbotForm(request.POST or None)
	return render(request, 'submit_code_five.html', {"form": form,})

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

			MYENCODING = 'utf-8'
			# http://stackoverflow.com/questions/3810302/python-unicode-popen-or-popen-error-reading-unicode
			'''
			When the source program is Python, you can use os.environ['PYTHONIOENCODING'] = 'utf-8' before the Popen. This environment variable instructs python to use UTF-8 as the default instead of ASCII. All Unicode characters can be sent with this encoding...just .decode('utf-8') the output received to turn in back to Unicode.
			'''
			os.environ['PYTHONIOENCODING'] = MYENCODING
			return_output = subprocess.check_output(["python", PY_DIR]) # bytes
			return HttpResponse('<br />' + return_output.decode(MYENCODING).replace('\n', '<br />'))
			return HttpResponse(json.dumps({'return_output': return_output}), content_type="application/json")
			

			# # http://stackoverflow.com/questions/2804543/read-subprocess-stdout-line-by-line
			# return_output = subprocess.Popen(["python", PY_DIR], stdout=subprocess.PIPE)
			# beautiful_return_output = []
			# while True:
			# 	line = return_output.stdout.readline()
			# 	if not line:
			# 		break
			# 	beautiful_return_output.append(line.decode("gb18030"))

			# return HttpResponse('\n'.join(beautiful_return_output))
			# # return HttpResponse(json.dumps({'beautiful_return_output': beautiful_return_output}), content_type="application/json")
	else:
		return render(request, 'submit_code_five.html', {"form": form,})
