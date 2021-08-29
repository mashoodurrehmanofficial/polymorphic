from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("login", views.loginx, name = "login"),
    path("logout", views.logoutx, name = "logout"),
    path("forgot", views.forgot, name = "forgot"),
    path("verification", views.verification, name = "verification"),
    url(r'^activate/(?P<uidb64>.+)/(?P<token>.+)/$',views.activateAccount, name='activateaccount'),
]