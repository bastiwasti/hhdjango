SELECT
        strftime('%Y',
        a.pub_date) as Jahr,
        strftime('%m',
        a.pub_date) as Monat,
        a.TYP,
        count(*) Anzahl,
        sum(a.Summe) Summe
    FROM
        hhdata_Ausgaben a
    group by
        a.typ,
        Jahr,
        Monat;