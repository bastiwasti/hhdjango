from django import forms

from hhdata.models import Transaktion

from django.db.models.functions import ExtractMonth, ExtractYear


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
