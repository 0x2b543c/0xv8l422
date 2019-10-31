import argparse
from typing import Dict, List, NamedTuple
from datetime import date, datetime, timedelta, time
from psycopg2.extras import NamedTupleCursor
from math import factorial
from collections import defaultdict
import sys
import psycopg2

from utils import valid_date

"""
A metric on active addresses in the trailing 1-year for the cryptos we’re studying (BTC, ETH, XRP, ZEC, XTZ, EOS, TRX, DOGE).
"""

parser = argparse.ArgumentParser(description="Returns active addresses over a given time interval (days).")
parser.add_argument('--host', type=str, required=True)
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--start', type=valid_date, required=True, help="YYYY-MM-DD")
parser.add_argument('--end', type=valid_date, required=True, help="YYYY-MM-DD")
parser.add_argument('--asset', type=str, required=True)
parser.add_argument('--days', type=int, required=True, help="Activity Window (in days)")

def get_active_addresses(host, port, asset, day):
    if asset in {"BTC", "BCH", "DOGE", "ZEC"}:
        return get_utxo_active_addresses(host, port, asset, day)
    elif asset in {"XTZ", "XRP"}:
        return get_balance_events_active_addresses(host, port, asset, day)
    elif asset in {"ETH"}:
        return get_transfers_active_addresses(host, port, asset, day)
    else:
        raise NotImplementedError("Unsupported asset {}".format(asset))


def get_balance_events_active_addresses(host, port, asset, day):
    with psycopg2.connect("postgresql://postgres@{}:{}/postgres-factory-production".format(host, port)) as conn:
        with conn.cursor() as cursor:
            end = day + timedelta(days = 1)
            cursor.execute("SELECT address FROM balance_events WHERE asset = %s AND time >= %s AND time < %s", (asset.upper(), day, end))
            return cursor.fetchall()


def get_transfers_active_addresses(host, port, asset, day):
    with psycopg2.connect("postgresql://postgres@{}:{}/postgres-factory-production".format(host, port)) as conn:
        with conn.cursor() as cursor:
            end = day + timedelta(days = 1)
            cursor.execute("""
                SELECT source FROM transfers WHERE asset = %s AND time >= %s AND time < %s
                UNION
                SELECT destination FROM transfers WHERE asset = %s AND time >= %s AND time < %s""", (asset.upper(), day, end, asset.upper(), day, end))
            return cursor.fetchall()


def get_utxo_active_addresses(host, port, asset, day):
    database = "postgres4" if asset in {"BTC", "BCH"} else "postgres3"
    time = "median_time" if asset in {"BTC", "BCH"} else "time"

    with psycopg2.connect("postgresql://postgres@{}:{}/{}".format(host, port, database)) as conn:
        with conn.cursor() as cursor:
            table = "{}_outputs".format(asset.lower())

            end = day + timedelta(days = 1)
            cursor.execute("""
                SELECT output_addresses[1] FROM {} WHERE output_{}_created >= %s AND output_{}_created < %s
                UNION
                SELECT output_addresses[1] FROM {} WHERE output_{}_spent >= %s AND output_{}_spent < %s""".format(table, time, time, table, time, time), (day, end, day, end))
            return cursor.fetchall()

if __name__ == "__main__":
    args = parser.parse_args()
    
    print("Day\tActive\tNew\tDead")

    # map of address to date of last activity
    active_addresses = {}

    current_date = args.start
    while current_date <= args.end:
        expiry = current_date - timedelta(days=args.days + 1)
        active = get_active_addresses(args.host, args.port, args.asset, current_date)
        added = 0

        for addr in active:
            if addr not in active_addresses:
                added += 1
            active_addresses[addr] = current_date

        to_expire = {addr for addr, activity in active_addresses.items() if activity <= expiry}
        removed = 0
        for addr in to_expire:
            present = active_addresses.pop(addr, None) is not None
            if present:
                removed += 1

        print("{}\t{}\t{}\t{}".format(current_date.date(), len(active_addresses), added, removed))
        sys.stdout.flush()
        current_date += timedelta(days=1)