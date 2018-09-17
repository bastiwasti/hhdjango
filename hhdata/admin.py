from django.contrib import admin

from .models import Transaktion, AusgabenPlan, Klassifizierung, Hierachie

class TransaktionAdmin(admin.ModelAdmin):
    list_display = ('Betrag','Typ','Auftraggeber','Buchungstext','Verwendungszweck','Buchung')

class AusgabenPlanAdmin(admin.ModelAdmin):
    list_display = ('Summe','Typ')

class KlassifizierungPlanAdmin(admin.ModelAdmin):
    list_display = ('Feld','Inhalt','Typ')

class HierachieAdmin(admin.ModelAdmin):
    list_display = ('Typ1','Typ2','Typ3')


admin.site.register(Transaktion, TransaktionAdmin)
admin.site.register(AusgabenPlan,AusgabenPlanAdmin)
admin.site.register(Klassifizierung,KlassifizierungPlanAdmin)
admin.site.register(Hierachie,HierachieAdmin)