from django.db import models
from datetime import date

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


class Ausgaben(models.Model):
    Summe = models.FloatField()
    Typ = models.CharField(
        max_length=21,
        choices=Typ)
    Person = models.CharField(
        max_length=20,
        choices=Person)
    Beschreibung = models.CharField(max_length=200)
    Zeitpunkt = models.DateField()
    User = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class AusgabenPlan(models.Model):
    Summe = models.FloatField()
    Typ = models.CharField(
        max_length=21,
        choices=Typ)
    Person = models.CharField(
        max_length=20,
        choices=Person)