from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from random import randint
import json
from .scrape import attendance
from .forms import AttendForm
from .gen import decrypt, encrypt
from .moodle_sel import moodle, assign
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    return render(request, 'landing.html')
def login(request):
        return HttpResponse(render(request, 'login.html'))

def get_name(request):
    # if this is a POST request we need to process the form data
    global check
    check="YES"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AttendForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            data = form.cleaned_data
            request.session['regid']=data['regid']
            request.session['passw']=data['passw']
            request.session['mood_reg']=data['mood_reg']
            request.session['mood_passw']=data['mood_passw']
            return HttpResponseRedirect('login/',request)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AttendForm()

    return render(request, 'attend.html', {'form': form})
@csrf_exempt
def apiassignment(request):
        return JsonResponse(assign(request.POST["hr"],request.POST["mood_reg"],request.POST["mood_passw"]), safe=False)
@csrf_exempt
def apiattend(request):
    if request.method=='POST':
        dic = attendance(request.POST['regid'], request.POST['passw'])
    else:
        dic = None
    return JsonResponse(dic, safe=False)

@csrf_exempt
def apimoodle(request):
    if request.method == 'POST':
        dic = moodle(request.POST['mood_reg'],request.POST['mood_passw'])
    else:
        dic = None
    return JsonResponse(dic,safe=False)
