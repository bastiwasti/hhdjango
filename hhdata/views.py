from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import IntegerField, F, Sum, Case, When


from hhdata.models import AusgabenPlan, Transaktion
from hhdata.utils import exec_sql,my_custom_sql,dictfetchall,write_data_to_django

@login_required()
def get_name(request):

    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        write_data_to_django(csvfile)

        posts = Transaktion.objects.all().order_by('-Buchung')
        pivot = exec_sql('hhdata\\querys.sql')
        return render(request, 'hhdata/index.html/', {'posts': posts, 'pivot': pivot})

    # if a GET (or any other method) we'll create a blank hhdata
    #else:

    pivot = exec_sql('hhdata\\querys.sql')

    posts = Transaktion.objects.all().order_by('-Buchung')
    return render(request, 'hhdata/index.html', {'posts': posts, 'pivot': pivot})


# todo classifier:
# classifier darüber legen, in web oberfläche oder davor?

# todo live gehen:
# project ist auf github, pythonanywhere account erstellt, config zu django app erstellen..
# wenn ab nächster woche 'in use' ergeben sich bestimmt neue anforderungen :)

# todo grafiken bauen:
# daten irgendwie visualisieren...
# evtl. kann ich neue tables erstellen und die dann direkt ansprechen?

# todo tabellen verbessern:
# wenn möglich dynamischen filter darauf setzen?
# mehrere monate werden abgezogen, zu jedem monat wird ein neuer tab erstellt
# evtl. jquery datatables versuchen zu initialisieren, der html part wird ähnlich aussehen könnte ich mir vorstellen?!

# todo csv export der gepflegten daten:
# per knopf soll es möglich sein, einen csv abzug der daten abzuziehen in einem für excel guten format