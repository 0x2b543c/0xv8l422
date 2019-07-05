import psycopg2
import argparse
import sys

from typing import List
from psycopg2.extras import NamedTupleCursor
from collections import namedtuple
from datetime import datetime, timedelta
from decimal import Decimal
from statistics import median, StatisticsError
from utils import valid_date, quantify

parser = argparse.ArgumentParser(description='Compute OP_RETURN statistics.')
parser.add_argument('--host', type=str, required=True)
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--start', type=valid_date, required=True, help="YYYY-MM-DD")
parser.add_argument('--end', type=valid_date, required=True, help="YYYY-MM-DD")
parser.add_argument('--asset', type=str, required=True)

OpReturnOutput = namedtuple('OpReturnOutput', ['tx', 'vout', 'script', 'value'])

def get_op_return_outputs(conn, asset: str, start: datetime, end: datetime) -> List[OpReturnOutput]:
    """
    Returns all OP_RETURN outputs for a given asset and time range
    """
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("""
            SELECT
                output_tx_hash "tx",
                output_index "vout",
                output_value_satoshi "value",
                ENCODE(output_script, 'hex') "script"
            FROM
                """ + asset + """_outputs
            WHERE
                output_median_time_created >= %s
            AND
                output_median_time_created < %s
            AND
                OCTET_LENGTH(output_script) > 0 
            AND 
                GET_BYTE(output_script, 0) = 106
        """, (start, end))
        return list(map(lambda rec: OpReturnOutput(rec.tx, rec.vout, rec.script, rec.value), cur.fetchall()))

if __name__ == "__main__":
    args = parser.parse_args()

    print("Day\tOutputs\tTransactions")

    current_date = args.start
    with psycopg2.connect("postgresql://postgres@{}:{}/postgres3".format(args.host, args.port)) as conn:
        while current_date <= args.end:
            outputs = get_op_return_outputs(conn, args.asset, current_date, current_date + timedelta(days=1))
            transactions = len({o.tx for o in outputs})
            print("{}\t{}\t{}".format(current_date.date(), len(outputs), transactions))
            sys.stdout.flush()
            current_date += timedelta(days=1)