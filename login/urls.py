from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.login_member),
    path('login/', views.login_member,name='login'),
    path('logout/', views.logout_member,name='logout'),
    path('make_account/',views.make_account,name='make_account'),
    path('mycalendar/', include('mycalendar.urls')),
    path('export/', include('export.urls')),

]
