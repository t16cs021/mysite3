from django.contrib import admin


from django.utils.translation import ugettext_lazy
from .models import Car, CarRecord, RefuelRecord, EtcRecord, CarReserve, CarMaintenance

# Register your models here.


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name','distance',)
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': ['distance']}),
    ]


@admin.register(CarRecord)
class CarRecordAdmin(admin.ModelAdmin):
    list_display = ('id','name','employee_number','start_date','end_date')

@admin.register(RefuelRecord)
class RefuelRecordAdmin(admin.ModelAdmin):
    list_display = ('refuel_key',)

@admin.register(EtcRecord)
class EtcRecordAdmin(admin.ModelAdmin):
    list_display = ('etc_key','date','section')

@admin.register(CarReserve)
class CarReserveAdmin(admin.ModelAdmin):
    list_display = ('name','employee_number',)

@admin.register(CarMaintenance)
class CarMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('name','start_date',)
