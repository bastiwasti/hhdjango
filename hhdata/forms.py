from django import forms
from django.forms import SelectDateWidget
from .models import Ausgaben
from datetime import date

class NameForm(forms.ModelForm):
    Zeitpunkt = forms.DateField(
    input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d' ],
    widget=SelectDateWidget(

    ), initial = date.today
)
    class Meta:
            model = Ausgaben
            fields = ['Summe','Typ','Person','Beschreibung','Zeitpunkt']