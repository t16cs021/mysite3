from django.urls import path, include

from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<int:year>/<int:month>/<int:day>/', login_required(views.Index.as_view()), name='car_index'),
    path('car_table/<int:year>/<int:month>/<int:day>/', login_required(views.CarTable.as_view()), name='car_table'), #車両
    path('car_record/<int:year>/<int:month>/<int:day>/', login_required(views.CarRecordIndex.as_view()), name='car_record'), #運行記録
    path('refuel_record/<int:year>/<int:month>/<int:day>/', login_required(views.RefuelRecordIndex.as_view()), name='refuel_record'), #給油記録
    path('etc_record/<int:year>/<int:month>/<int:day>/', login_required(views.EtcRecordIndex.as_view()), name='etc_record'), #ETC記録
    path('car_reserve/<int:year>/<int:month>/<int:day>/', login_required(views.CarReserveIndex.as_view()), name='car_reserve'), #車両予約
    path('car_maintenance/<int:year>/<int:month>/<int:day>/', login_required(views.CarMaintenanceIndex.as_view()), name='car_maintenance'), #メンテナンス予約
    path('my_record/<int:year>/<int:month>/<int:day>/', login_required(views.MyRecord.as_view()), name='my_record'), #ユーザの運行記録など一覧
    path('my_reserve/<int:year>/<int:month>/<int:day>/', login_required(views.MyReserve.as_view()), name='my_reserve'), #ユーザの予約一覧


]
