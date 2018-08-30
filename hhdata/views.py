from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import IntegerField, F, Sum, Case, When


from .forms import NameForm
from hhdata.models import Ausgaben, AusgabenPlan
from hhdata.utils import exec_sql,my_custom_sql,dictfetchall

@login_required()
def get_name(request):
    # if this is a POST request we need to process the hhdata data
    if request.method == 'POST' and 'add' in request.POST:
        # create a hhdata instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Eintrag.objects.filter(Name=request.user).delete()
            ausgaben = form.save(commit=False)
            # process the data in hhdata.cleaned_data as required
            # ...
            # redirect to a new URL:
            ausgaben.User = request.user  # Set the user object here
            ausgaben.pub_date = timezone.now()  # Set the user object here
            ausgaben.save()

            return HttpResponseRedirect(request.path)  # generate an empty hhdata

    if request.method == 'POST' and 'delete' in request.POST:
        Ausgaben.objects.filter(id=request.POST['pk']).delete()
        # return HttpResponseRedirect(request.path)

    if request.method == 'POST' and 'update' in request.POST:
        ausgaben = Ausgaben.objects.get(id=request.POST['pk'])
        form = NameForm(instance=ausgaben)
        posts = Ausgaben.objects.filter(User=request.user)
        Ausgaben.objects.filter(id=request.POST['pk']).delete()
        pivot = exec_sql('hhdata\\querys.sql')
        return render(request, 'hhdata/index.html/', {'form': form, 'posts': posts, 'pivot': pivot})


    # if a GET (or any other method) we'll create a blank hhdata
    else:
        form = NameForm()

    pivot = exec_sql('hhdata\\querys.sql')

    posts = Ausgaben.objects.filter(User=request.user)
    return render(request, 'hhdata/index.html', {'form': form, 'posts': posts, 'pivot': pivot})

# todo live gehen:
# git projekt auf github füllen, pythonanywhere neuen account erstellen und frei verfügbar machen
# wenn ab nächster woche 'in use' ergeben sich bestimmt neue anforderungen :)

# todo api zu bank:
# checken ob bank logins nicht doch irgendwie verfügbar sind... würde komplett andere möglichkeiten geben

# todo grafiken bauen:
# daten irgendwie visualisieren...
# evtl. kann ich neue tables erstellen und die dann direkt ansprechen?

# todo tabellen verbessern:
# wenn möglich dynamischen filter darauf setzen?
# mehrere monate werden abgezogen, zu jedem monat wird ein neuer tab erstellt
# evtl. jquery datatables versuchen zu initialisieren, der html part wird ähnlich aussehen könnte ich mir vorstellen?!

# todo csv export der gepflegten daten:
# per knopf soll es möglich sein, einen csv abzug der daten abzuziehen in einem für excel guten format