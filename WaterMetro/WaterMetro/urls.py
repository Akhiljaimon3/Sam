"""
URL configuration for WaterMetro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('watermetro-login', views.login),
    path('watermetro-bookyourjourney', views.bookyourjourney),
    path('watermetro-applyforconcession', views.applyforconcession),
    path('watermetro-signup', views.signup),
    path('watermetro-resetpassword/<token>', views.reset_password),
    path('watermetro-forgotpassword', views.forgot_password),
    path('watermetro-youraccount', views.youraccount),
    path('adminhome', views.adminhome),
    path('addroute', views.addroute),
    path('editroute', views.editroute),
    path('deleteroute', views.deleteroute),
    path('editroutelist', views.editroutelist),
    path('bookingreport', views.bookingreport),
    path('concessionreport', views.concessionreport),
    path('concessionrequests', views.concessionrequests),
    path('concessiondiscount', views.concessiondiscount),
    path('deleteroutetable', views.deleteroutetable),
    path('watermetro-aboutus', views.aboutus),
    path('watermetro-terminals-vytilla', views.terminalsvytilla),
    path('watermetro-terminals-chernalloor', views.terminalschernalloor),
    path('watermetro-terminals-eloor', views.terminalseloor),
    path('watermetro-terminals-fortkochi', views.terminalsfortkochi),
    path('watermetro-terminals-highcourt', views.terminalshighcourt),
    path('watermetro-terminals-kakkanad', views.terminalskakkanad),
    path('watermetro-terminals-southchitoor', views.terminalssouthchitoor),
    path('watermetro-terminals-vypin', views.terminalsvypin),
    path('watermetro-concessionpayment/<str:email>', views.concessionpayment),
    path('watermetro-ticketpayment', views.ticketpayment),
    path('watermetro-ticketview', views.ticketview),
    path('watermetro-concessionview', views.concessionview),
    path('logout', views.logout),
    path('editaccount', views.editaccount),
    path('deletediscount', views.deletediscount),
    path('concessionpay/<int:id>',views.concessionpay),
    path('ticketpay/<int:id>',views.ticketpay),
    path('bookingsuccess', views.bookingsuccess),
    path('concessionsuccess', views.concessionsuccess),
    path('dbchanger', views.dbchanger),
    path('account-changepw', views.accountchangepassword),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


