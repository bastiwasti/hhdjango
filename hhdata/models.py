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


class AusgabenPlan(models.Model):
    Summe = models.FloatField()
    Typ = models.CharField(
        max_length=21,
        choices=Typ)
    Person = models.CharField(
        max_length=20,
        choices=Person)


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
        max_length=200)
    Inhalt = models.CharField(
        max_length=200)
    Typ = models.CharField(
        max_length=200,
        choices=Typ)