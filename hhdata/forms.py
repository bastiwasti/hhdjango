from django import forms
from django.forms import SelectDateWidget
from datetime import date
from hhdata.models import Transaktion
from hhdata.utils import exec_sql
from django.db.models.functions import ExtractMonth, ExtractYear

# class MyForm(forms.Form):
#     like = forms.ChoiceField(
#         queryset= Transaktion.objects.annotate(yearmonth=ExtractYear('Buchung'),
#     month=ExtractMonth('Buchung')).distinct().order_by('-yearmonth', '-month')\
#        .values_list("yearmonth", "month"),
#         initial=0
#     )
#
#    # exec_sql('hhdata\\querys_time.sql')
# #
# # from django.db.models.functions import ExtractMonth, ExtractYear
# #
# #    Transaktion.objects.annotate(yearmonth=ExtractYear('Buchung'),
# #     month=ExtractMonth('Buchung')).distinct().order_by('-yearmonth', '-month')\
# #        .values_list("yearmonth", "month")
# #
# #
# # \
# #
# #
# #        .only('year','month')
#
# from django.db.models.functions import Concat
# from django.db.models import Value as V
#
# Transaktion.objects.annotate(yearmonth=Concat(ExtractYear('Buchung'),
#     ExtractMonth('Buchung'))).distinct().order_by('-yearmonth').values_list("yearmonth")
#
#
# ['%i-%02i' % (x.Buchung.year, x.Buchung.month) for x in Transaktion.objects.order_by('-Buchung')]


from django.db.models.functions import ExtractMonth, ExtractYear


# class MyForm(forms.Form):
#     my_choice_field = forms.ChoiceField()
#
#     # ...
#
#     def __init__(self, *args, **kwargs):
#         super(MyForm, self).__init__(*args, **kwargs)
#         qs = Transaktion.objects.annotate(
#             year=ExtractYear('Buchung'),
#             month=ExtractMonth('Buchung')
#         ).order_by('-year', '-month').values('year','month').distinct()
#         self.fields['my_choice_field'].choices = [row['year'] * 100 + row['month'] for row in qs]
#

def get_my_choices():
    qs = Transaktion.objects.annotate(
    year=ExtractYear('Buchung'),
    month=ExtractMonth('Buchung')).order_by('-year', '-month').values('year','month').distinct()

    out = [(row['year'] * 100 + row['month'], '{}-{:02d}'.format(row['year'], row['month']))
         for row in qs
    ]

    return out

class MyForm(forms.Form):
    my_choice_field = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['my_choice_field'] = forms.ChoiceField(
            choices=get_my_choices() )
