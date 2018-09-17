from django.db import models

Typ = (
    ('LEH', 'LEH'),
    ('Drogerie', 'Drogerie'),
    ('Lieferant', 'Lieferant'),
    ('Essengehen', 'Essengehen'),
    ('Sonstiges für Wohnung', 'Sonstiges für Wohnung'),
    ('Benzin', 'Benzin'),
    ('Taschengeld', 'Taschengeld'),
    ('Jette', 'Jette'),
)

Person = (
    ('Corinna', 'Corinna'),
    ('Basti', 'Basti'),
    ('Gemeinsam', 'Gemeinsam'),
)

TransFeld = (
    ('Auftraggeber', 'Auftraggeber'),
    ('Buchungstext', 'Buchungstext'),
    ('Verwendungszweck', 'Verwendungszweck'),
)

class Transaktion(models.Model):
    Betrag = models.FloatField()
    Typ = models.CharField(
        max_length=200)
    Auftraggeber = models.CharField(
        max_length=200)
    Buchungstext = models.CharField(
        max_length=200)
    Verwendungszweck = models.CharField(max_length=200)
    Buchung = models.DateField()


class Klassifizierung(models.Model):
    Feld = models.CharField(
        max_length=200,
        choices=TransFeld)
    Inhalt = models.CharField(
        max_length=200)
    Typ = models.CharField(
        max_length=200)


from django.utils.functional import lazy

def get_menu_choices():
    choices_tuple = [(q['Typ'], q['Typ']) for q in Klassifizierung.objects.values('Typ').distinct()]
    return choices_tuple

class Hierachie(models.Model):

    Typ1 = models.CharField(max_length=200, blank=True)
    Typ2 = models.CharField(max_length=200, blank=True)
    Typ3 = models.CharField(max_length=200, blank=True)

    def __init__(self,  *args, **kwargs):
        super(Hierachie, self).__init__(*args, **kwargs)
        self._meta.get_field('Typ1').choices = lazy(get_menu_choices, list)()

def get_typ():
    choices_tuple = [(q['Typ2'], q['Typ2']) for q in Hierachie.objects.values('Typ2').distinct()]
    return choices_tuple

class AusgabenPlan(models.Model):
    Summe = models.FloatField()
    Typ = models.CharField(
        max_length=21)

    def __init__(self,  *args, **kwargs):
        super(AusgabenPlan, self).__init__(*args, **kwargs)
        self._meta.get_field('Typ').choices = lazy(get_typ, list)()

