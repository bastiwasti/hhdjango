select
    a.Jahr,
    a.Monat,
    a.Typ,
    Anzahl,
    Summe,
    Gesamt,
    Gesamt-Summe
from
    ( SELECT
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
        Monat         ) a
join
    (
        select
            typ,
            sum(Summe) as Gesamt
        from
            hhdata_AusgabenPlan
        group by
            typ
    ) b
        on a.typ = b.typ;