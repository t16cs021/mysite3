
import csv
import io
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from .forms import CSVUploadForm
from .models import Post 
from mycalendar.models  import  CarRecord,RefuelRecord,EtcRecord
from mycalendar import mixins

class PostIndex_veh(mixins.MonthCalendarMixin,generic.ListView):
    template_name = 'export/index_veh.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        carrecord = CarRecord.objects.all()
        page_context = {
            "page_name": "car_table",
            "carrecord": carrecord,
        }
        context.update(page_context)

        return context




class PostIndex_ref(mixins.MonthCalendarMixin,generic.ListView):
    template_name = 'export/index_ref.html'
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        refrecord = RefuelRecord.objects.all()
        page_context = {
            "page_name": "car_table",
            "refrecord": refrecord,
        }
        context.update(page_context)

        return context


class PostIndex_etc(mixins.MonthCalendarMixin,generic.ListView):
    template_name = 'export/index_etc.html'
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        etcrecord = EtcRecord.objects.all()
        page_context = {
            "page_name": "car_table",
            "etcrecord": etcrecord,
        }
        context.update(page_context)

        return context





class PostImport(generic.FormView):
    template_name = 'export/import.html' , 'index_ref.html'
    success_url = reverse_lazy('export:index_ref')
    form_class = CSVUploadForm
 
    def form_valid(self, form):
        # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
        csvfile = io.TextIOWrapper(form.cleaned_data['file'])
        reader = csv.reader(csvfile)
        # 1行ずつ取り出し、作成していく
        for row in reader:
            post, created = Post.objects.get_or_create(pk=row[0])
            post.title = row[1]
            post.save()
        return super().form_valid(form)


def veh_post_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="veh.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    for item in CarRecord.objects.all():
        writer.writerow([item.name,item.employee_number,item.start_date,item.end_date,item.start_distance,item.end_distance,item.destination,item.content])
    return response



def ref_post_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ref.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    for item in RefuelRecord.objects.all():
        writer.writerow([item.refuel_key, item.start_date, item.date, item.location, item.distance, item.amount])
    return response

def etc_post_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="etc.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    for item in EtcRecord.objects.all():
        writer.writerow([item.etc_key, item.date, item.section])
    return response
