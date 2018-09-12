from django.contrib import admin

from .models import Transaktion, AusgabenPlan, Klassifizierung

class TransaktionAdmin(admin.ModelAdmin):
    list_display = ('Betrag','Typ','Auftraggeber','Buchungstext','Verwendungszweck','Buchung')

class AusgabenPlanAdmin(admin.ModelAdmin):
    list_display = ('Summe','Typ','Person')

class KlassifizierungPlanAdmin(admin.ModelAdmin):
    list_display = ('Feld','Inhalt','Typ')

admin.site.register(Transaktion, TransaktionAdmin)
admin.site.register(AusgabenPlan,AusgabenPlanAdmin)
admin.site.register(Klassifizierung,KlassifizierungPlanAdmin)