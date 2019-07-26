from typing import List, NamedTuple
from datetime import date, datetime, timedelta, time
from psycopg2.extras import NamedTupleCursor


class Transfer(NamedTuple):
    time: datetime
    source: str
    destination: str
    value: float
    transfer_type: str


def get_transfers(conn, asset: str, day: date) -> List[Transfer]:
    """
    Returns all transfers for a given asset and day
    """
    start = datetime.combine(day, time())
    end = datetime.combine(day + timedelta(days=1), time())

    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("""
            SELECT
                time,
                source,
                destination,
                value,
                type "transfer_type"
            FROM
                transfers
            WHERE
                asset = %s
            AND
                time >= %s
            AND
                time < %s
        """, (asset, start, end))
        return list(map(lambda rec: Transfer(rec.time, rec.source, rec.destination, rec.value, rec.transfer_type), cur.fetchall()))