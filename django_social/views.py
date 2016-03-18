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

def confirmation(request):
    return render(request,'confirmation.html')

def home(request):
    return render_to_response('index.html')

from .forms import NameForm

def get_name(request):
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            return submit(request,form.cleaned_data.get('myname'),form.cleaned_data.get('myfood'),form.cleaned_data.get('towhere'),form.cleaned_data.get('fromwhere'))
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'index.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('/')


def submit(request,myname,myfood,towhere,fromwhere):
    headeroauth = OAuth1(client_key, client_secret,
                     resource_owner_key, resource_owner_secret,
                     signature_type='auth_header')
    



    userurl='https://api.twitter.com/1.1/account/verify_credentials.json'
    userinfo=requests.get(userurl,auth=headeroauth).json()
    theid=userinfo["id_str"]
    screen_name=userinfo["screen_name"]

    #print(theid)
    url='https://api.twitter.com/1.1/direct_messages/new.json?'
    
    
    friendsURL='https://api.twitter.com/1.1/friends/ids.json'
    params={'screen_name':screen_name,'count':200,}
    friendsresponse=requests.get(friendsURL,params=params,auth=headeroauth).json()
    friendslist=friendsresponse["ids"]

    followsURL = 'https://api.twitter.com/1.1/followers/ids.json'
    followsresponse=requests.get(followsURL,params=params,auth=headeroauth).json()
    followslist=followsresponse["ids"]

    friendfollows = []
    for e in friendslist:
        if e in followslist:
            friendfollows.append(e);

    #count=0
    #frienddict={}
    #for userobject in friendlist:
    #    if (count==5):
    #        break
    #    key=str(count)+"name"
    #    frienddict[key]=userobject['name']
    #    frienddict[str(count)+key]=userobject['screen_name']
    #    count+=1
    #print(frienddict)
    userURL = 'https://api.twitter.com/1.1/users/show.json'
    frienddict = {}
    i = 0
    while i < 5 and i < len(friendfollows):
        x = friendfollows[i]
        frienddict[str(i)+'name'] = requests.get(userURL, params = {'user_id': x}, auth = headeroauth).json()['name']

        postdata = {
        'text': myname+" is asking for "+myfood+" from "+fromwhere+" delivered to "+towhere+". Thanks!" ,
        'user_id': x,
        }
        #r = requests.post(url, data=postdata,auth=headeroauth)
        i = i + 1
        
    #print(r.text)
    return render(request,'confirmation.html',context=frienddict)
    
    