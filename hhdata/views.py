from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import IntegerField, F, Sum, Case, When

from django.db.models.functions import Concat, ExtractMonth, ExtractYear

from hhdata.forms import  MyForm
from hhdata.models import AusgabenPlan, Transaktion
from hhdata.utils import exec_sql,my_custom_sql,dictfetchall,write_data_to_django,UpdateClassify


@login_required()
def get_name(request):

    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        write_data_to_django(csvfile)

        posts = Transaktion.objects.all().order_by('-Buchung')
        pivot = exec_sql('hhdata/querys.sql')
        form = MyForm(request.POST)
        pivot2 = exec_sql('hhdata/querys_typ2.sql')
        return render(request, 'hhdata/index.html', {'form': form, 'posts': posts, 'pivot': pivot, 'pivot2': pivot2})

    if request.POST and 'update' in request.POST:
        UpdateClassify()
        posts = Transaktion.objects.all().order_by('-Buchung')
        pivot = exec_sql('hhdata/querys.sql')
        form = MyForm(request.POST)
        pivot2 = exec_sql('hhdata/querys_typ2.sql')
        return render(request, 'hhdata/index.html', {'form': form, 'posts': posts, 'pivot': pivot, 'pivot2': pivot2})
    # if a GET (or any other method) we'll create a blank hhdata
    #else:

    if request.POST and 'filter' in request.POST:
        form = MyForm(request.POST)

        if form.is_valid():
            check = form.cleaned_data['my_choice_field']

            if len(str(check)[4:]) == 1:
                check2 = '0' + str(check)[4:]
            else:
                check2 = str(check)[4:]

            posts = Transaktion.objects.filter(Buchung__year=int(str(check)[:4]), Buchung__month=int(str(check)[4:])).order_by('-Buchung')
            pivot = exec_sql('hhdata/querys.sql')
            pivot = [d for d in pivot if d['Jahr'] in str(check)[:4] and d['Monat'] in check2]
            pivot2 = exec_sql('hhdata/querys_typ2.sql')
            pivot2 = [d for d in pivot2 if d['Jahr'] in str(check)[:4] and d['Monat'] in check2]
            return render(request, 'hhdata/index.html',
                          {'form': form, 'posts': posts, 'pivot': pivot, 'pivot2': pivot2})

    form = MyForm()
    posts = Transaktion.objects.all().order_by('-Buchung')
    pivot = exec_sql('hhdata/querys.sql')
    pivot2 = exec_sql('hhdata/querys_typ2.sql')
    return render(request, 'hhdata/index.html', {'form': form, 'posts': posts, 'pivot': pivot, 'pivot2': pivot2})

# todo view rewrite:
# best practise ansehen wie views richtig aufgesetzt werden,
# nur eine funktion hier drin macht keinen sinn und müsste ich besser wissen...

# todo tabellen verbessern:
# wenn möglich dynamischen filter darauf setzen?
# mehrere monate werden abgezogen, zu jedem monat wird ein neuer tab erstellt
# evtl. jquery datatables versuchen zu initialisieren, der html part wird ähnlich aussehen könnte ich mir vorstellen?!

# todo grafiken bauen:
# daten irgendwie visualisieren...
# evtl. kann ich neue tables erstellen und die dann direkt ansprechen?
