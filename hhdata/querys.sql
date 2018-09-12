select
    a.Jahr,
    a.Monat,
    a.Typ,
    Anzahl,
    Betrag,
    Gesamt,
    Gesamt+Betrag Rest
from
    ( SELECT
        strftime('%Y',
        a."Buchung") as Jahr,
        strftime('%m',
        a."Buchung") as Monat,
        a.TYP,
        count(*) Anzahl,
        sum(a.Betrag) Betrag
    FROM
        hhdata_transaktion a
    group by
        a.typ,
        Jahr,
        Monat         ) a
left join
    (
        select
            typ,
            sum(Summe) as Gesamt
        from
            hhdata_AusgabenPlan
        group by
            typ
    ) b
        on a.typ = b.typ
        order by jahr desc, monat desc;

--SELECT
--        strftime('%Y',
--        a."Buchung") as Jahr,
--        strftime('%m',
--        a."Buchung") as Monat,
--        a.TYP,
--        Buchung,
--        a.Betrag Betrag
--    FROM
--        hhdata_transaktion a

