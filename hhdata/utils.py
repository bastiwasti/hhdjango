from django.db import connection
import pandas as pd
import numpy as np
from hhdata.models import Transaktion, Klassifizierung


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



# df = pd.read_csv('..//Umsatzanzeige_DE93500105175421917214_20180831.csv',sep=";"
#                    ,skiprows = 11, encoding = 'cp1252', decimal=",")
#
# df['Betrag'] = (df['Betrag'].str.split()).apply(lambda x: float(x[0].replace('.', '').replace(',', '.')))
# df['Buchung'] = pd.to_datetime(df['Buchung'])
# df['Valuta'] = pd.to_datetime(df['Buchung'])
#
# df['test'] = df['Betrag']
# # Klassifizierung einbauen!
# # soll über django gemanaged werden...
#
# conditions = [
#     df['Auftraggeber/Empfänger'].str.upper().str.contains('LIDL') |
#     df['Auftraggeber/Empfänger'].str.upper().str.contains('ZUG UM ZUG') |
#     df['Auftraggeber/Empfänger'].str.upper().str.contains('REWE') |
#     df['Auftraggeber/Empfänger'].str.upper().str.contains('FLEISCHER'),
#     df['Auftraggeber/Empfänger'].str.upper().str.contains('ANNELIESE KOETTING')
# ]
# choices = ['LEH','Miete']
#
# df['Typ'] = np.select(conditions,choices, default='Nicht vergeben')
#
# df = df.rename(columns={'Auftraggeber/Empfänger': 'Auftraggeber'})
#
# df.groupby(['Typ']).agg(['count'])
#
# df.dtypes
#
#
# dfinsert.dtypes
# # Daten müssen in SQLite DB gespielt werden..
# # Model muss angepasst werden
#
# from hhdata.models import Transaktion
#
# for rows in df.itertuples():
#     Transaktion.objects.create(Betrag = rows.Betrag,
#                             Typ = rows.Typ,
#                             Auftraggeber = rows.Auftraggeber,
#                             Buchungstext = rows.Buchungstext,
#                             Verwendungszweck=rows.Verwendungszweck,
#                             Buchung = rows.Buchung )
#
# # das funktioniert sogar :D
#
# # muss gedanken machen, welche felder ich speichern will -
# # identifier ist am besten der gesamte export
# # darüber wird gecheckt, ob ein eintrag schon vorhanden ist!
# # zusätzlich spalten einbauen die zur klassifikation genutzt werden etc.
#
# # dann muss ich das ganze in django integrieren in irgendeiner form,
# # idee war csv upload starten und dann werden alle zeilen eingelesen
# # und abgeglichen..
#
# Transaktion.objects.all().delete()
#
# dfdjango = pd.DataFrame(list(Transaktion.objects.all().values()))
# dfdjango['Buchung'] = pd.to_datetime(dfdjango['Buchung'])
#
# # so easy.....
#
# dfinsert = pd.merge(df, dfdjango, on=['Betrag','Buchungstext','Auftraggeber','Buchung']
#                   ,how='left')
# dfinsert = dfinsert[dfinsert['Typ_y'].isna()].to_string()
#
# if not isinstance(dfinsert,str):
#     for rows in dfinsert.itertuples():
#         Transaktion.objects.create(Betrag=rows.Betrag,
#                                    Typ=rows.Typ_x,
#                                    Auftraggeber=rows.Auftraggeber,
#                                    Buchungstext=rows.Buchungstext,
#                                    Verwendungszweck=rows.Verwendungszweck_x,
#                                    Buchung=rows.Buchung)
#
# # Funktion aus bruchstücken schreiben
#
# file = '..//Umsatzanzeige_DE13701633700004119339_20180831.csv'

def write_data_to_django(file):
    # CSV einlesen:
    df = pd.read_csv(file, sep=";"
                     , skiprows=11, encoding='cp1252', decimal=",")

    # Types
    df['Betrag'] = (df['Betrag'].str.split()).apply(lambda x: float(x[0].replace('.', '').replace(',', '.')))
    df['Buchung'] = pd.to_datetime(df['Buchung'], format='%d.%m.%Y')

    df = df.rename(columns={'Auftraggeber/Empfänger': 'Auftraggeber'})
    df = df.replace(np.NaN,'')

    df = classify(df)

    # Momentanen Datenstand einlesen:
    dfdjango = pd.DataFrame(list(Transaktion.objects.all().values()))
    if not dfdjango.__len__() == 0:
        dfdjango['Buchung'] = pd.to_datetime(dfdjango['Buchung'])

        # Nur neue Zeilen behalten
        dfinsert = pd.merge(df, dfdjango, on=['Betrag', 'Buchungstext', 'Auftraggeber', 'Buchung']
                            , how='left')
        dfinsert = dfinsert[dfinsert['Typ_y'].isna()]
    else:
        dfinsert = df.rename(columns={'Typ': 'Typ_x',
                                      'Verwendungszweck': 'Verwendungszweck_x'})

    # Insert in SQL Table
    if not isinstance(dfinsert, str):
        for rows in dfinsert.itertuples():
            Transaktion.objects.create(Betrag=rows.Betrag,
                                       Typ=rows.Typ_x,
                                       Auftraggeber=rows.Auftraggeber,
                                       Buchungstext=rows.Buchungstext,
                                       Verwendungszweck=rows.Verwendungszweck_x,
                                       Buchung=rows.Buchung)


# Transaktion.objects.all().delete()
# #
#  dfdjango = pd.DataFrame(list(Transaktion.objects.all().values()))
# #
# # write_data_to_django('..//Umsatzanzeige_DE93500105175421917214_20180831.csv')
#
# df = pd.read_csv('..//Umsatzanzeige_DE93500105175421917214_20180831.csv',sep=";"
#                    ,skiprows = 11, encoding = 'cp1252', decimal=",")
#
# df['Betrag'] = (df['Betrag'].str.split()).apply(lambda x: float(x[0].replace('.', '').replace(',', '.')))
# df['Buchung'] = pd.to_datetime(df['Buchung'], format='%d.%m.%Y')
# df['Valuta'] = pd.to_datetime(df['Buchung'])
#
# df
#

def UpdateClassify():
    df1 = pd.DataFrame(list(Transaktion.objects.all().values()))
    df2 = classify(pd.DataFrame(list(Transaktion.objects.all().values())))

    dfinsert = pd.merge(df1, df2, on=['id']
                        , how='inner')
    dfinsert['check'] = np.where((dfinsert['Typ_x'] != dfinsert['Typ_y']),1,0)
    df3 = dfinsert[dfinsert['check']==1]

    Transaktion.objects.filter(id__in = list(dfinsert[dfinsert['check']==1]['id'])).delete()

    if not isinstance(df3, str):
        for rows in df3.itertuples():
            Transaktion.objects.create(Betrag=rows.Betrag_x,
                                       Typ=rows.Typ_y,
                                       Auftraggeber=rows.Auftraggeber_x,
                                       Buchungstext=rows.Buchungstext_x,
                                       Verwendungszweck=rows.Verwendungszweck_x,
                                       Buchung=rows.Buchung_x)


def classify(data):
    conditions = list()
    for n in range(0,Klassifizierung.objects.count()):
        conditions.append(data[list(Klassifizierung.objects.values_list('Feld', flat=True))[n]].str.contains(list(Klassifizierung.objects.values_list('Inhalt', flat=True))[n]))

    choices = list(Klassifizierung.objects.values_list('Typ',flat=True))

    data['Typ'] = np.select(conditions, choices, default='Nicht vergeben')
    return data

