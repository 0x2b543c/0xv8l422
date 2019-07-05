import psycopg2
import argparse

from typing import List
from psycopg2.extras import NamedTupleCursor
from collections import namedtuple, defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
from statistics import median, StatisticsError
from utils import valid_date, quantify


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
        return list(map(lambda rec: Transfer(rec.source, rec.destination, rec.value, rec.time, rec.type, rec.chain), cur.fetchall()))


def adjusted_volume(transfers: List[Transfer]) -> Decimal:
    """
    Given all the transaction that happened in a single day,
    computes the adjusted transaction volume for that day
    """

    # first group transactions by hour
    transfers_per_hour = defaultdict(list)
    for transfer in filter(lambda t: t.value > 0, transfers):
        transfers_per_hour[transfer.time.replace(minute=0, second=0, microsecond=0)].append(transfer)

    # for each batch, compute the raw incoming volume and net balance change of each address
    # if the net balance change is 0, do not count the address's raw incoming volume
    adjusted_volume = 0

    for batch in transfers_per_hour.values():
        balance_change = defaultdict(int)
        incoming_value = defaultdict(int)

        for transfer in batch:
            incoming_value[transfer.destination] += transfer.value
            balance_change[transfer.destination] += transfer.value
            balance_change[transfer.source] -= transfer.value

        for (addr, value) in incoming_value.items():
            net_balance_change = balance_change[addr]
            if net_balance_change != 0:
                adjusted_volume += value

    return adjusted_volume
        

if __name__ == "__main__":
    args = parser.parse_args()
    # Print header
    print("Day\tKIN2Creations\tKIN3Creations\tKIN2Payments\tKIN3Payments\tKIN2Volume\tKIN3Volume\tKIN2AdjVolume\tKIN3AdjVolume\tKIN2MedianPayment\tKIN3MedianPayment")
    current_date = args.start
    with psycopg2.connect("postgresql://postgres@{}:{}/postgres2".format(args.host, args.port)) as conn:
        while current_date <= args.end:
            transfers = get_transfers(conn, current_date, current_date + timedelta(days=1))
            kin2_creations = quantify(transfers, lambda t: t.chain == 'kin2' and t.type == 'CREATE')
            kin3_creations = quantify(transfers, lambda t: t.chain == 'kin3' and t.type == 'CREATE')

            kin2_payments = quantify(transfers, lambda t: t.chain == 'kin2' and t.type == 'PAYMENT')
            kin3_payments = quantify(transfers, lambda t: t.chain == 'kin3' and t.type == 'PAYMENT')

            kin2_volume = sum([t.value for t in transfers if t.chain == 'kin2'])
            kin3_volume = sum([t.value for t in transfers if t.chain == 'kin3'])

            kin2_adjvolume = adjusted_volume([t for t in transfers if t.chain == 'kin2'])
            kin3_adjvolume = adjusted_volume([t for t in transfers if t.chain == 'kin3'])

            try:
                kin2_median_payment = median([t.value for t in transfers if t.chain == 'kin2' and t.type == 'PAYMENT'])
            except StatisticsError:
                kin2_median_payment = ""

            try:
                kin3_median_payment = median([t.value for t in transfers if t.chain == 'kin3' and t.type == 'PAYMENT'])
            except StatisticsError:
                kin3_median_payment = ""

            print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                current_date.date(), 
                kin2_creations, 
                kin3_creations, 
                kin2_payments, 
                kin3_payments,
                kin2_volume,
                kin3_volume,
                kin2_adjvolume,
                kin3_adjvolume,
                kin2_median_payment,
                kin3_median_payment
            ))

            current_date += timedelta(days=1)