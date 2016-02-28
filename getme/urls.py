"""getme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
     url('', include('social.apps.django_app.urls', namespace='social')),
     url(r'^$', 'django_social.views.login'),

    url(r'^home/$', 'django_social.views.home'),
    url(r'^logout/$', 'django_social.views.logout'),
    url(r'^submit/$','django_social.views.submit' ),
    url(r'^twitter/$','django_social.views.twitter' ),
    url(r'^complete/twitter$','django_social.views.callback' ),
    url(r'^confirmation/$','django_social.views.get_name' ),
]
