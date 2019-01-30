from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from typing import List

class Car(models.Model):
    name = models.CharField(_('車両名'), max_length=20, unique=True)
    distance = models.CharField(_('走行距離数'), max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('車両')
        verbose_name_plural = _('車両')


class CarRecord(models.Model):
    name = models.CharField(_('車両名'),max_length=20)
    employee_number = models.CharField(_('社員番号'),max_length=20)
    start_date = models.DateTimeField(_('開始日時'),default=timezone.now)
    end_date = models.DateTimeField(_('終了日時'),default=timezone.now)
    start_distance = models.CharField(_('開始時の走行距離数'),max_length=20)
    end_distance = models.CharField(_('終了時の走行距離数'),max_length=20)
    destination = models.CharField(_('行き先'),max_length=20)
    content = models.CharField(_('メンテナンス内容'),max_length=200)

    def get_refuel_list(self):
        record_id = self.id
        tmp_refuel_list = RefuelRecord.objects.filter(id__startswith=record_id) 
        print(tmp_refuel_list)
        refuel_list = list()
        refuel_list = tmp_refuel_list
        return refuel_list

    def get_etc_list(self):
        etc_list = List()
        return etc_list

    def __str__(self):
        return self.name

    def is_date(self, year, month, day):
        s = timezone.localtime(self.start_date)
        e = timezone.localtime(self.end_date)
        return (s.year == year and s.month == month and s.day == day) or (e.year == year and e.month == month and e.day == day)

    def is_print(self):
        s = timezone.localtime(self.start_date)
        e = timezone.localtime(self.end_date)
        print(str(s.year) + ":" + str(s.month) + ":" + str(s.day) + ":" + str(s.hour) + "," + str(e.year) + ":" + str(e.month) + ":" + str(e.day) + ":" + str(e.hour))

    class Meta:
        verbose_name = _('運行記録')
        verbose_name_plural = _('運行記録')

class RefuelRecord(models.Model):
    refuel_key = models.CharField(_('給油キー'),max_length=20) #対応する運行記録のidを格納する
    date = models.CharField(_('給油日'),max_length=20)
    location = models.CharField(_('給油場所'),max_length=20)
    distance = models.CharField(_('給油時の走行距離数'),max_length=20)
    amount = models.CharField(_('給油量'),max_length=20)

    def __str__(self):
        return str(self.refuel_key)

    class Meta:
        verbose_name = _('給油記録')
        verbose_name_plural = _('給油記録')

class EtcRecord(models.Model):
    etc_key = models.CharField(_('ETCキー'),max_length=20) 
    date = models.DateField(_('ETC利用日'),default=timezone.now)
    section = models.CharField(_('走行区間'),max_length=20)

    def __str__(self):
        return str(self.etc_key)

    class Meta:
        verbose_name = _('ETC記録')
        verbose_name_plural = _('ETC記録')

class CarReserve(models.Model):
    name = models.CharField(_('車両名'),max_length=20,unique=True)
    employee_number = models.CharField(_('社員番号'),max_length=20)
    start_date = models.DateTimeField(_('開始日時'),default=timezone.now)
    end_date = models.DateTimeField(_('終了日時'),default=timezone.now)
    destination = models.CharField(_('行き先'),max_length=20)
    etc_key = models.CharField(_('ETC利用キー'),max_length=20)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = _('車両予約')
        verbose_name_plural = _('車両予約')

class CarMaintenance(models.Model):
    name = models.CharField(_('車両名'),max_length=20,unique=True)
    start_date = models.DateTimeField(_('開始日時'),default=timezone.now)
    end_date = models.DateTimeField(_('終了日時'),default=timezone.now)
    content = models.CharField(_('メンテナンス内容'),max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('メンテナンス予約')
        verbose_name_plural = _('メンテナンス予約')
