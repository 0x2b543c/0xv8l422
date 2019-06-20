import psycopg2
import argparse

from typing import List
from psycopg2.extras import NamedTupleCursor
from collections import namedtuple
from datetime import datetime, timedelta

def quantify(seq, pred=None):
    "Count how many times the predicate is true in the sequence"
    return sum(map(pred, seq))

# https://stackoverflow.com/questions/25470844/specify-format-for-input-arguments-argparse-python
def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser(description='Process KIN transfers.')
parser.add_argument('--host', type=str)
parser.add_argument('--port', type=int)
parser.add_argument('--start', type=valid_date, help="YYYY-MM-DD")
parser.add_argument('--end', type=valid_date, help="YYYY-MM-DD")


Transfer = namedtuple('Transfer', ['source', 'destination', 'value', 'time', 'type', 'chain'])

# Returns all transfers between start and end
def get_transfers(conn, start: datetime, end: datetime) -> List[Transfer]:
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT source, destination, value, time, type, chain FROM kin_transfers WHERE time >= %s AND time < %s", (start, end))
        return map(lambda rec: Transfer(rec.source, rec.destination, rec.value, rec.time, rec.type, rec.chain), cur.fetchall())


if __name__ == "__main__":
    args = parser.parse_args()
    # Print header
    print("Day\tKIN2Creations\tKIN3Creations\tKIN2Payments\tKIN3Payments")
    current_date = args.start
    with psycopg2.connect("postgresql://postgres@{}:{}/postgres2".format(args.host, args.port)) as conn:
        while current_date <= args.end:
            transfers = get_transfers(conn, current_date, current_date + timedelta(days=1))
            kin2_creations = quantify(transfers, lambda t: t.chain == 'kin2' and t.type == 'CREATE')
            kin3_creations = quantify(transfers, lambda t: t.chain == 'kin3' and t.type == 'CREATE')

            kin2_payments = quantify(transfers, lambda t: t.chain == 'kin2' and t.type == 'PAYMENT')
            kin3_payments = quantify(transfers, lambda t: t.chain == 'kin3' and t.type == 'PAYMENT')

            print("{}\t{}\t{}\t{}\t{}".format(current_date, kin2_creations, kin3_creations, kin2_payments, kin3_payments))
            current_date += timedelta(days=1)