SELECT
        strftime('%Y',
        a."Buchung") as Jahr,
        strftime('%m',
        a."Buchung") as Monat,
        typ3,
        count(*) Anzahl,
        sum(a.Betrag) Betrag
    FROM
        hhdata_transaktion a
        left join hhdata_hierachie b on a.typ = b.typ1
    group by
        typ3,
        Jahr,
        Monat