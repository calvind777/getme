from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from requests_oauthlib import OAuth1
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect,HttpResponse

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
import requests
from requests_oauthlib import OAuth1Session
redirect_uri = 'https://www.twitter.com'
# from django.template.context import RequestContext
from config import *

resource_owner_key=''
resource_owner_secret=''
verifier=''



@csrf_exempt
def login(request):
    # context = RequestContext(request, {
    #     'request': request, 'user': request.user})
    # return render_to_response('login.html', context_instance=context)
    c = {}
    c.update(csrf(request))
    return render(request, 'login.html',c)

@ensure_csrf_cookie
@csrf_protect
def twitter(request):
    print(8)
    c = {}
    c.update(csrf(request))
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    oauth = OAuth1Session(client_key, client_secret=client_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    global resource_owner_key
    resource_owner_key = fetch_response.get('oauth_token')
    global resource_owner_secret 
    resource_owner_secret  = fetch_response.get('oauth_token_secret')
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorize_url = base_authorization_url + '?oauth_token='
    authorize_url = authorize_url + resource_owner_key
    redirect_response=HttpResponseRedirect(authorize_url)
    return redirect_response

@ensure_csrf_cookie
@csrf_protect
def callback(request):
    c = {}
    
    c.update(csrf(request))
    
    
    uri = request.build_absolute_uri()
    
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    oauth = OAuth1Session(client_key, client_secret=client_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    global resource_owner_secret
    resource_owner_secret  = fetch_response.get('oauth_token_secret')
    
    oauth_response=oauth.parse_authorization_response(uri)
    
    global verifier 
    verifier = oauth_response.get('oauth_verifier')

    
    global resource_owner_key
    resource_owner_key=oauth_response.get('oauth_token')

    access_token_url = 'https://api.twitter.com/oauth/access_token'

    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    
    global resource_owner_key
    resource_owner_key = oauth_tokens.get('oauth_token')
    
    global resource_owner_secret
    resource_owner_secret  = oauth_tokens.get('oauth_token_secret')


    
    return render_to_response('index.html',c)



def home(request):
    return render_to_response('index.html')



def logout(request):
    auth_logout(request)
    return redirect('/')


def submit(request):
    headeroauth = OAuth1(client_key, client_secret,
                     resource_owner_key, resource_owner_secret,
                     signature_type='auth_header')
    url='https://api.twitter.com/1.1/direct_messages/new.json?'
    print(5)
    
    postdata = {
    'text': 'http://www.google.com',
    'screen_name': 'jamelao118',
    }
    r = requests.post(url, data=postdata,auth=headeroauth)
    print(r.text)
    return render_to_response('index.html')
    
    