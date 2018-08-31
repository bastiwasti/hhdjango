from django.contrib import admin

from .models import Transaktion, AusgabenPlan

class TransaktionAdmin(admin.ModelAdmin):
    list_display = ('Betrag','Typ','Auftraggeber','Buchungstext','Verwendungszweck','Buchung')

class AusgabenPlanAdmin(admin.ModelAdmin):
    list_display = ('Summe','Typ','Person')


admin.site.register(Transaktion, TransaktionAdmin)
admin.site.register(AusgabenPlan,AusgabenPlanAdmin)