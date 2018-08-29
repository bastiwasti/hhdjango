from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import IntegerField, F, Sum, Case, When
from django.db import connection


from .forms import NameForm
from hhdata.models import Ausgaben, AusgabenPlan

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


def exec_sql(path):
    fd = open(path, 'r')
    string = fd.read()
    build = string.replace('\n',' ')
    return my_custom_sql(build)

def my_custom_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = dictfetchall(cursor)
    return row

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# todo funktionen auslagern:
# funktionen wenn möglich soweit auslagern, dass sie mit einem source befehl oder ähnlichem bei konsolenstart eingelesen
# werden können

# todo api zu bank:
# checken ob bank logins nicht doch irgendwie verfügbar sind... würde komplett andere möglichkeiten geben

# todo live gehen:
# git projekt auf github füllen, pythonanywhere neuen account erstellen und frei verfügbar machen
