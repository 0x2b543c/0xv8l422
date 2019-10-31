import argparse
from typing import Dict, List, NamedTuple
from datetime import date, datetime, timedelta, time
from psycopg2.extras import NamedTupleCursor
from math import factorial
from collections import defaultdict
import sys
import psycopg2

from utils import valid_date


class BitcoinInput(NamedTuple):
    txid: str
    vout: int

class BitcoinOutput(NamedTuple):
    value: int
    script: str


parser = argparse.ArgumentParser(description='Returns an estimation of BIP-69 usage over time.')
parser.add_argument('--host', type=str, required=True)
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--start', type=valid_date, required=True, help="YYYY-MM-DD")
parser.add_argument('--end', type=valid_date, required=True, help="YYYY-MM-DD")
parser.add_argument('--asset', type=str, required=True)

def bn_to_hash(bn: int) -> str:
    return "{:x}".format(int(bn)).zfill(64)

def get_inputs(cursor, asset: str, day: date) -> Dict[str, BitcoinInput]:
    start = datetime.combine(day, time())
    end = datetime.combine(day + timedelta(days=1), time())

    cursor.execute("""
        SELECT
            output_spending_tx_hash "tx",
            output_tx_hash "hash",
            output_index "index"
        FROM
            {}_outputs
        WHERE
            output_median_time_spent >= '{}'
        AND
            output_median_time_spent < '{}'
        """.format(asset.lower(), start, end))
    
    records = cursor.fetchall()
    
    ret = defaultdict(list)
    for rec in records:
        tx = bn_to_hash(rec.tx)
        ret[tx].append(BitcoinInput(bn_to_hash(rec.hash), rec.index))

    return ret


def get_outputs(cursor, asset: str, day: date) -> Dict[str, BitcoinOutput]:
    start = datetime.combine(day, time())
    end = datetime.combine(day + timedelta(days=1), time())

    cursor.execute("""
        SELECT
            output_tx_hash "tx",
            output_value_satoshi "value",
            ENCODE(output_script, 'hex') "script"
        FROM
            {}_outputs
        WHERE
            output_median_time_created >= '{}'
        AND
            output_median_time_created < '{}'
        """.format(asset.lower(), start, end))

    records = cursor.fetchall()

    ret = defaultdict(list)
    for rec in records:
        tx = bn_to_hash(rec.tx)
        ret[tx].append(BitcoinOutput(int(rec.value), rec.script))

    return ret

def sorted_tuples(tuples):
    return list(sorted(tuples, key=lambda t: (t[0], t[1])))


def is_bip_69(inputs: List[BitcoinInput], outputs: List[BitcoinOutput]) -> bool:
    """Returns whether the transaction complies to BIP-69,
    lexicographical ordering of inputs and outputs"""
 
    # Quick check
    if len(inputs) == 1 and len(outputs) == 1:
        return True

    input_keys = [(i.txid, i.vout) for i in inputs]

    if sorted_tuples(input_keys) != input_keys:
        return False

    output_keys = [(o.value, o.script) for o in outputs]

    return sorted_tuples(output_keys) == output_keys

if __name__ == "__main__":
    args = parser.parse_args()
    # print("Day\tT\tC\tTRetail\tCRetail\tTLargeInputs\tCLargeInputs\tTCJ\tCCJ")

    current_date = args.start
    with psycopg2.connect("postgresql://postgres@{}:{}/postgres4".format(args.host, args.port)) as conn:
        while current_date <= args.end:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                outputs = get_outputs(cursor, args.asset, current_date)
                inputs = get_inputs(cursor, args.asset, current_date)

                n = 0
                n_large_inputs = 0
                n_coinjoin = 0
                n_retail = 0

                compliant = 0
                compliant_large_inputs = 0
                compliant_coinjoin = 0
                compliant_retail = 0

                for tx in outputs:
                    vout = outputs[tx]
                    if tx not in inputs:
                        continue

                    vin = inputs[tx]

                    n += 1

                    c = is_bip_69(vin, vout)
                    if c:
                        compliant += 1

                    large_inputs = len(vin) >= 5
                    coinjoin = large_inputs and len(vout) >= 5 and abs(len(vout) - len(vin)) <= 2
                    retail = len(vout) <= 2 and len(vin) <= 3

                    if large_inputs:
                        n_large_inputs += 1

                    if large_inputs and c:
                        compliant_large_inputs += 1

                    if coinjoin:
                        n_coinjoin += 1
                    if coinjoin and c:
                        compliant_coinjoin += 1
                    
                    if retail:
                        n_retail += 1
                    if retail and c:
                        compliant_retail += 1
                    
                print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(current_date.date(), n, compliant, n_retail, compliant_retail, n_large_inputs, compliant_large_inputs, n_coinjoin, compliant_coinjoin))
                sys.stdout.flush()
                current_date += timedelta(days=1)