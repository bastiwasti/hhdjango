from django.contrib import admin

from .models import Ausgaben, AusgabenPlan

class AusgabenAdmin(admin.ModelAdmin):
    list_display = ('User','Summe','Typ','Person','Beschreibung','Zeitpunkt','pub_date')

class AusgabenPlanAdmin(admin.ModelAdmin):
    list_display = ('Summe','Typ','Person')


admin.site.register(Ausgaben, AusgabenAdmin)
admin.site.register(AusgabenPlan,AusgabenPlanAdmin)