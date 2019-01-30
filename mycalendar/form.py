from django import forms

from .models import Car, CarRecord, RefuelRecord, EtcRecord, CarReserve, CarMaintenance

class CarForm(forms.ModelForm):
    name = forms.ModelChoiceField(label='車両',queryset=Car.objects.all())

    class Meta:
        model = Car
        fields = ('name','distance',)

class CarRecordForm(forms.ModelForm):
    name = forms.ModelChoiceField(label='車両',queryset=Car.objects.all()) #これで、Carインスタンスからのみ選択可能なプルダウンになる。
    start_date = forms.SplitDateTimeField(label='開始時刻')
    end_date = forms.SplitDateTimeField(label='終了時刻')

    class Meta:
        model = CarRecord
        fields = ('employee_number','start_distance','end_distance','destination',)

class RefuelRecordForm(forms.ModelForm):

    class Meta:
        model = RefuelRecord
        fields = ('date','location','distance','amount',)

class EtcRecordForm(forms.ModelForm):

    class Meta:
        model = EtcRecord
        fields = ('date','section',)

class CarReserveForm(forms.ModelForm):
    name = forms.ModelChoiceField(label='車両',queryset=Car.objects.all())
    start_date = forms.SplitDateTimeField(label='開始時刻')
    end_date = forms.SplitDateTimeField(label='終了時刻')

    class Meta:
        model = CarRecord
        fields = ('employee_number','destination',) #全要素指定は,fields = '__all__'だが、上記と重複するので、必要なものだけにする。


class CarMaintenanceForm(forms.ModelForm):
    name = forms.ModelChoiceField(label='車両',queryset=Car.objects.all())
    start_date = forms.SplitDateTimeField(label='開始時刻')
    end_date = forms.SplitDateTimeField(label='終了時刻')

    class Meta:
        model = CarRecord
        fields = ('content',)


    
