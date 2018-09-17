select
    a.Jahr,
    a.Monat,
    a.Typ2,
    a.Typ3,
    Anzahl,
    Betrag,
    Plan,
    Plan+Betrag Rest
from
    ( SELECT
        strftime('%Y',
        a."Buchung") as Jahr,
        strftime('%m',
        a."Buchung") as Monat,
        typ2,
        typ3,
        count(*) Anzahl,
        sum(a.Betrag) Betrag
    FROM
        hhdata_transaktion a
        left join hhdata_hierachie b on a.typ = b.typ1
    group by
        typ2,
        typ3,
        Jahr,
        Monat ) a
left join
    (
        select
            typ,
            sum(Summe) as Plan
        from
            hhdata_AusgabenPlan
        group by
            typ
    ) b
        on a.typ2 = b.typ

