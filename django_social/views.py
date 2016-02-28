from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login
import requests
redirect_uri = 'http://www.twitter.com'
# from django.template.context import RequestContext


def login(request):
    # context = RequestContext(request, {
    #     'request': request, 'user': request.user})
    # return render_to_response('login.html', context_instance=context)
    return render(request, 'login.html')


@login_required(login_url='/')
def home(request):
    return render_to_response('index.html')



def logout(request):
    auth_logout(request)
    return redirect('/')

def submit(request):
    url='https://api.twitter.com/1.1/direct_messages/new.json?'
    
    print(5)
    postdata = {
    'text': 'trigger fingers turn to twitter fingers',
    'screen_name': 'jamelao118',
    }
    r = requests.post(url, data=postdata)
    print(r.text)
    return redirect('/')
    
    