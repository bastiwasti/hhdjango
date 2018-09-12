select
    distinct
    strftime('%Y',a."Buchung") || "-" ||
    strftime('%m',a."Buchung") as YearMonth
from
    hhdata_transaktion a
order by
    1 desc