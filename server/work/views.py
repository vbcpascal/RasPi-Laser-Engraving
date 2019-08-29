from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from work.forms import ProfileForm, PrintForm
from work.models import Image, Text

import os

# Create your views here.


def index(request):
    context = {}
    form = ProfileForm
    context['form'] = form
    template = loader.get_template('work/index.html')
    return HttpResponse(template.render(context, request))


def print(request):
    if request.method == 'POST':
        f = ProfileForm(request.POST, request.FILES)
        if f.is_valid():
            img = Image()
            img.name = f.cleaned_data['name']
            img.pic = f.cleaned_data['pic']
            img.user = f.cleaned_data['user']
            img.save()

            os.system('python3 ' + os.path.join('../', 'main.py ') +
                      '-m work -f ' + os.path.join('./', 'uploads/') + img.pic.name)

            context = {}
            form = PrintForm
            context['form'] = form
            template = loader.get_template('work/print.html')
            return HttpResponse(template.render(context, request))
        else:
            return redirect(to='index')
    return redirect(to='index')
