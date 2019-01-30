from django.urls import path
from . import views

app_name = 'export'

urlpatterns = [
    path('veh/', views.PostIndex_veh.as_view(), name='index_veh'),
    path('ref/', views.PostIndex_ref.as_view(), name='index_ref'),
    path('etc/', views.PostIndex_etc.as_view(), name='index_etc'),
    path('import/', views.PostImport.as_view(), name='import'),
    path('veh-export/', views.veh_post_export, name='veh-export'),
    path('ref-export/', views.ref_post_export, name='ref-export'),
    path('etc-export/', views.etc_post_export, name='etc-export'),
]