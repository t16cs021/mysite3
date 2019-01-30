from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from .form import CarForm, CarRecordForm,CarReserveForm, RefuelRecordForm, EtcRecordForm,  CarMaintenanceForm
from .models import Car, CarRecord, RefuelRecord, EtcRecord, CarReserve
from . import mixins
from datetime import timezone, timedelta
from django.utils import timezone
import datetime

from django.http import HttpResponse




class Index(mixins.MonthCalendarMixin, generic.TemplateView):

    template_name = 'mycalendar/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        page_context = {
            "page_name": "",
            "superuser_text": get_authority_status(self.request)
        }
        context.update(page_context)

        return context



class CarTable(mixins.MonthCalendarMixin, generic.TemplateView):

    template_name = 'mycalendar/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        page_context = {
            "page_name": "car_table",
            "superuser_text": get_authority_status(self.request),
            "cars": Car.objects.all(),
        }
        context.update(page_context)

        return context


class CarRecordIndex(mixins.MonthCalendarMixin, generic.TemplateView):

    template_name = 'mycalendar/index.html'

    def post(self, request, *args, **kwargs): #postされるとここが実行される。

        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        form_name = request.POST['form_name']
        form_number = request.POST['form_number']

        if form_name == "record_form":
            s0 = request.POST['start_date_0']
            s1 = request.POST['start_date_1']
            e0 = request.POST['end_date_0']
            e1 = request.POST['end_date_1']
            car_name = (Car.objects.get(id=request.POST['name'])).name
            form = CarReserveForm(request.POST)
            if form.is_valid():
                item = form.save()
                item.start_date = s0 + ' ' + s1
                item.end_date = e0 + ' ' + e1
                if item.start_date >= item.end_date: #日付逆転チェック
                    print("日付逆転")
                    item.delete()
                    return render(request, self.template_name, self.get_context_data(**kwargs))
                item.name = car_name
                item.save()
                print("save")

                #車両重複チェック
                record_check = True
                car_record_check = CarRecord.objects.all()
                item2 = CarRecord.objects.get(id = item.id) #item.save()した後、再取得しないとdatetime型になっていない
                for item3 in car_record_check:
                    print(is_in_date(item2,item3))
                    if is_in_date(item2,item3):
                        if item2.id != item3.id and item2.name == item3.name:
                            print("車両重複")
                            (CarRecord.objects.get(id=item2.id)).delete()
                            return render(request, self.template_name, self.get_context_data(**kwargs))
                
                return render(request, self.template_name, self.get_context_data(**kwargs))

        else:
            form = CarMaintenanceForm(request.POST)
            if form.is_valid():
                item = form.save()

                return render(request, self.template_name, self.get_context_data(**kwargs))

        return render(request, self.template_name, self.get_context_data(**kwargs))



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        car_record_form = CarRecordForm()
        

        if self.kwargs.get('day')-1 == 0: #0日になるのを防ぐ用
            car_record_prev = CarRecord.objects.filter(start_date__startswith=datetime.date(self.kwargs.get('year'), self.kwargs.get('month'),1))
        
        else:
            car_record_prev = CarRecord.objects.filter(start_date__startswith=datetime.date(self.kwargs.get('year'), self.kwargs.get('month'),self.kwargs.get('day')-1)) #タイムゾーンのずれによって一日前に戻っているものがあるから、一日前のものももってくる.下記のitem.is_date(self.kwargs.get('year'), self.kwargs.get('month'), self.kwargs.get('day'))で不要なものは排除している。
        
        car_record_today = CarRecord.objects.filter(start_date__startswith=datetime.date(self.kwargs.get('year'), self.kwargs.get('month'), self.kwargs.get('day')))
        car_record = [item for item in car_record_prev] #QuerySetをlist化
        car_record_prev = [item for item in car_record_today]
        car_record.extend(car_record_prev) #listを結合

        send_record = []  # id、重複数、これ以降に重複したものをappend(末尾に要素を追加)していく。一個目の要素が[0]になっているので注意


        while len(car_record) != 0:
            if car_record[0].is_date(self.kwargs.get('year'), self.kwargs.get('month'),self.kwargs.get('day')):  # is_dateはmodels.pyで定義。指定された日付のデータかをチェック。常にデータが先頭にいくので、インデックスは0でよい(ss[0])
                l = duplicate_cal(car_record,car_record[0])
                record_list = []
                for item in range(len(l)):
                    l[item].start_date = timezone.localtime(l[item].start_date)
                    if not (l[item].start_date.year == self.kwargs.get('year') and l[item].start_date.month == self.kwargs.get('month') and l[item].start_date.day == self.kwargs.get('day')):
                        l[item].start_date = datetime.datetime(self.kwargs.get('year'), self.kwargs.get('month'), self.kwargs.get('day'), 0, 0, 0) #開始時刻が前日にある場合は、当日の0:00に調整。スケジュール表示用。範囲外には表示できないため。
                    l[item].end_date = timezone.localtime(l[item].end_date)
                    if not (l[item].end_date.year == self.kwargs.get('year') and l[item].end_date.month == self.kwargs.get('month') and l[item].end_date.day == self.kwargs.get('day')):
                        l[item].end_date = datetime.datetime(self.kwargs.get('year'), self.kwargs.get('month'),self.kwargs.get('day'), 23, 59,59)  #修了時刻が前日にある場合は、当日の0:00に調整。スケジュール表示用。範囲外には表示できないため。
                    now = datetime.datetime.now()
                    record_list.append({
                        "pos_x": 10 + (90/(len(l)+1) * (item+1)), #横座標。cssのleft x%のｘにあたる.
                        "pos_y": 65 -20 + 33 * l[item].start_date.hour, #縦座標。cssのtop ypxのyにあたる
                        "image_url": "/static/mycalendar/images/arrow_bottom_" + str(l[item].end_date.hour - l[item].start_date.hour ) + ".png", #画像のurl。何時間なのかを計算し、どの画像を利用するかを決める。追記：車両名のサイズぶん、上に移動。(-10)
                        "len": 32 * (l[item].end_date.hour - l[item].start_date.hour ), #上記の長さから、矢印の長さを計算
                        "record_item": l[item], #CarRecordモデルのインスタンス。ここに記録データが入っている。
                        "is_past": is_past(l[item]), #過去の情報かどうかを判定
                    }) #templateで扱いやすいように、map型にしてある。
                send_record.append({"record_list": record_list}) #templateで扱いやすいように、map型にしてある。
            else:
                car_record.remove(car_record[0])

        num_list = [item for item in range(24)] #テンプレートで時刻分ループする用

        page_context = {
            "num_list": num_list,
            "page_name": "car_record",
            "superuser_text": get_authority_status(self.request),
            "send_record": send_record,
            "car_record_form": car_record_form,
        }
        context.update(page_context)

        return context


#A->B->Cのように重複してる場合や、A->B->Cかつ、A->H->Fのように分岐重複している場合に対応
#listと重複のルートとなる要素を渡す。
def duplicate_cal(target_list, target_item):
    save_list = []
    save_list.append(target_item)
    target_list.remove(target_item)
    for item in target_list:
        if item != target_item and is_in_date(item,target_item):
            save_list.extend(duplicate_cal(target_list,item))
    return save_list



def is_in_date(date1, date2): #日付から時間（hourのみ)をみて、重複しているかどうかを判定する。
    start1 = timezone.localtime(date1.start_date) #localtime()にすることで、setting.pyで設定したlocaltimeに変換される。これをしないと9時間ぐらいずれる。
    start2 = timezone.localtime(date2.start_date)
    end1 = timezone.localtime(date1.end_date)
    end2 = timezone.localtime(date2.end_date)
    if not ((start1.year > end2.year or start1.month > end2.month or start1.day > end2.day or ((start1.year == end2.year and start1.month == end2.month and start1.day == end2.day) and (start1.hour > end2.hour))) or (end1.year < start2.year or end1.month < start2.month or end1.day < start2.day or ((end1.year == start2.year and end1.month == start2.month and end1.day == start2.day) and (end1.hour < start2.hour)))) :
        return True
    return False


def is_past(date):
    now = datetime.datetime.now()
    end = date.end_date

    if end.year < now.year or ((end.year == now.year) and end.month < now.month) or ((end.year == now.year and end.month == now.month) and end.day < now.day) :
        return True
    return False




class RefuelRecordIndex(mixins.MonthCalendarMixin, generic.TemplateView):

    template_name = 'mycalendar/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        page_context = {
            "page_name": "refuel_record",
            "superuser_text": get_authority_status(self.request),
            "refuel_record": RefuelRecord.objects.all(),
        }
        context.update(page_context)
        return context
    
class EtcRecordIndex(mixins.MonthCalendarMixin, generic.TemplateView):

    template_name = 'mycalendar/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        page_context = {
            "page_name": "etc_record",
            "superuser_text": get_authority_status(self.request),
            "etc_record": EtcRecord.objects.all(),
        }
        context.update(page_context)

        return context


class CarReserveIndex(mixins.MonthCalendarMixin, generic.TemplateView):

    template_name = 'mycalendar/index.html'

    def post(self, request, *args, **kwargs): #postされるとここが実行される。
        form = CarReserveForm(request.POST)

        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        if form.is_valid():
            item = form.save()
            item.name = (Car.objects.get(id=request.POST['name'])).name
            s0 = request.POST['start_date_0']
            s1 = request.POST['start_date_1']
            item.start_date = s0 + " " + s1
            e0 = request.POST['end_date_0']
            e1 = request.POST['end_date_1']
            item.end_date = e0 + " " + e1
            
            print(item.start_date)
            item.save()
            item2 = CarRecord.objects.get(id=item.id)

            form = CarReserveForm()        
            page_context = {
                "warning_text": "予約に成功しました。このまま再度予約可能です。",
                "page_name": "car_reserve",
                "superuser_text": get_authority_status(self.request),
                "form": form,
            }
            context.update(page_context)

            #車両重複チェック
            record_check = True
            car_record_check = CarRecord.objects.all()
            print(car_record_check[0].start_date)
            for item3 in car_record_check:
                print(item3)
                if is_in_date(item2,item3):
                    if item2.id != item3.id and item2.name == item3.name: #自分自身とも比較するので、idが異なることも条件とする
                        print("delete")
                        (CarRecord.objects.get(id=item2.id)).delete()
                        record_check = False
                        page_context = {
                            "warning_text": "予約に失敗しました。同一車両の予約時間が重複しています",
                            "page_name": "car_reserve",
                            "superuser_text": get_authority_status(self.request),
                            "form": form,
                        }
                        context.update(page_context)
                        return render(request, self.template_name, context)

            if item.start_date >= item.end_date and record_check:#日付逆転チェック
                page_context = {
                    "warning_text": "予約に失敗しました。開始時刻と終了時刻が逆転しています",
                    "page_name": "car_reserve",
                    "superuser_text": get_authority_status(self.request),
                    "form": form,
                }
                context.update(page_context)
                return render(request, self.template_name, context)
                
            return render(request, self.template_name, context)

        form = CarReserveForm()        
        page_context = {
            "warning_text": "予約に失敗しました。入力形式が間違っている可能性があります。",
            "page_name": "car_reserve",
            "superuser_text": get_authority_status(self.request),
            "form": form,
        }
        context.update(page_context)
        return render(request, self.template_name, context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        form = CarReserveForm()
        
        page_context = {
            "page_name": "car_reserve",
            "superuser_text": get_authority_status(self.request),
            "form": form,
        }
        context.update(page_context)

        return context


class CarMaintenanceIndex(mixins.MonthCalendarMixin, generic.TemplateView):

    template_name = 'mycalendar/index.html'

    def post(self, request, *args, **kwargs): #postされるとここが実行される。
        form = CarMaintenanceForm(request.POST)

        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        if form.is_valid():
            form.save()

            form = CarMaintenanceForm()        
            page_context = {
                "warning_text": "予約に成功しました。このまま再度予約可能です。",
                "page_name": "car_maintenance",
                "superuser_text": get_authority_status(self.request),
                "form": form,
            }
            context.update(page_context)
            return render(request, self.template_name, context)

        form = CarMaintenanceForm()        
        page_context = {
            "warning_text": "予約に失敗しました。入力形式が間違っている可能性があります。",
            "page_name": "car_maintenance",
            "superuser_text": get_authority_status(self.request),
            "form": form,
        }
        context.update(page_context)
        return render(request, self.template_name, context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        form = CarMaintenanceForm()
        
        page_context = {
            "page_name": "car_maintenance",
            "superuser_text": get_authority_status(self.request),
            "form": form,
        }
        context.update(page_context)

        return context



class MyRecord(mixins.MonthCalendarMixin, generic.TemplateView):

    template_name = 'mycalendar/index.html'

    def post(self, request, *args, **kwargs): #postされるとここが実行される。
        refuel_form = RefuelRecordForm(request.POST)
        etc_form = EtcRecordForm(request.POST)

        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        if refuel_form.is_valid():
            item = refuel_form.save()
            item.refuel_key = self.request.POST['key']
            item.save()

            return render(request, self.template_name, self.get_my_record_context(request, self.template_name, context))


        if etc_form.is_valid():
            item = etc_form.save()
            item.etc_key = self.request.POST['key']
            item.save()

            return render(request, self.template_name, self.get_my_record_context(request, self.template_name, context))

        return render(request, self.template_name, self.get_my_record_context(request, self.template_name, context))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        return self.get_my_record_context(self.request, self.template_name, context)


    def get_my_record_context(self, request, template_name, context):
        car_records = CarRecord.objects.filter(employee_number__startswith=self.request.user.username)
        past_reserve_list = []
        for item in car_records:
            if not (is_past(item)):
                past_reserve_list.append(item)
        record_list = []
        for item in past_reserve_list:
            refuel_records = RefuelRecord.objects.filter(refuel_key__startswith=item.id)
            etc_records = EtcRecord.objects.filter(etc_key__startswith=item.id)
            refuel_form = RefuelRecordForm()
            etc_form = EtcRecordForm()
            record_list.append({
                "refuel_form": refuel_form,
                "etc_form": etc_form,
                "car_record": item,
                "refuel_records": refuel_records,
                "etc_records": etc_records,
                
            })
        page_context = {
            "record_list": record_list,
            "page_name": "my_record",
            "superuser_text": get_authority_status(self.request)
        }
        context.update(page_context)
        return context


class MyReserve(mixins.MonthCalendarMixin, generic.TemplateView):

    template_name = 'mycalendar/index.html'


    def post(self, request, *args, **kwargs): #postされるとここが実行される。

        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        item = self.request.POST['key']
        remove_target_record = CarRecord.objects.get(id=item)
        remove_target_record.delete()

        return render(request, self.template_name, self.get_my_reserve_context(request, self.template_name, context))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        return self.get_my_reserve_context(self.request, self.template_name, context)


    def get_my_reserve_context(self, request, template_name, context):
        car_reserve = CarRecord.objects.filter(employee_number__startswith=self.request.user.username)
        reserve_list = []
        for item in car_reserve:
            if not (is_past(item)):
                reserve_list.append(item)
        record_list = []
        for item in reserve_list:
            record_list.append({
                "car_record": item,
                
            })
        page_context = {
            "record_list": record_list,
            "page_name": "my_reserve",
            "superuser_text": get_authority_status(self.request)
        }
        context.update(page_context)
        return context




def get_authority_status(request):
    superuser_text = "通常"
    if request.user.is_superuser:
        superuser_text = "管理者"
    return superuser_text

