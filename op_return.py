import psycopg2
import argparse
import sys

from typing import List
from psycopg2.extras import NamedTupleCursor
from collections import namedtuple, Counter
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

def compute_stats(args):
    print("Day\tOutputs\tTransactions")

    current_date = args.start
    with psycopg2.connect("postgresql://postgres@{}:{}/postgres3".format(args.host, args.port)) as conn:
        while current_date <= args.end:
            outputs = get_op_return_outputs(conn, args.asset, current_date, current_date + timedelta(days=1))
            transactions = len({o.tx for o in outputs})
            print("{}\t{}\t{}".format(current_date.date(), len(outputs), transactions))
            sys.stdout.flush()
            current_date += timedelta(days=1)

def protocol_counter(args):
    print("Day\tProtocol\tOutputs")
    current_date = args.start
    with psycopg2.connect("postgresql://postgres@{}:{}/postgres3".format(args.host, args.port)) as conn:
        while current_date <= args.end:
            outputs = get_op_return_outputs(conn, args.asset, current_date, current_date + timedelta(days=1))
            protocol_counter = Counter([protocol_mapper(o.script) for o in outputs])
            others = len(outputs) - sum(map(lambda x: x[1], protocol_counter.most_common(5)))
            for prot, count in protocol_counter.most_common(5):
                print("{}\t{}\t{}".format(current_date.date(), prot, count))
            print("{}\tOthers\t{}".format(current_date.date(), others))
            sys.stdout.flush()
            current_date += timedelta(days=1)

prefixes = [
    ["6a4c5000", "Veriblock"],
    ["6a146f6d6e", "Omni"],
    ["6a026d01", "memo.cash"],
    ["6a026d02", "memo.cash"],
    ["6a026d03", "memo.cash"],
    ["6a026d04", "memo.cash"],
    ["6a026d05", "memo.cash"],
    ["6a026d06", "memo.cash"],
    ["6a026d07", "memo.cash"],
    ["6a026d0a", "memo.cash"],
    ["6a026d0b", "memo.cash"],
    ["6a026d0c", "memo.cash"],
    ["6a026d0d", "memo.cash"],
    ["6a026d0e", "memo.cash"],
    ["6a026d10", "memo.cash"],
    ["6a026d13", "memo.cash"],
    ["6a026d14", "memo.cash"],
    ["6a026d16", "memo.cash"],
    ["6a026d17", "memo.cash"],
    ["6a026d24", "memo.cash"],
    ["6a026d30", "memo.cash"],
    ["6a026d31", "memo.cash"],
    ["6a026d32", "memo.cash"],
    ["6a0400000010", "Tokeda"],
    ["6a0400000020", "Tokenized"],
    ["6a040000005C", "BCHTorrents"],
    ["6a0400001337", "GameChain Lobby"],
    ["6a04000015B3", "Satchat"],
    ["6a04000022B8", "Turingnote"],
    ["6a0400004b50", "Keoken Platform"],
    ["6a040000544C", "TradeLayer"],
    ["6a040000B006", "Bookchain"],
    ["6a0400031337", "GameChain"],
    ["6a0400242424", "Cashies"],
    ["6a0400666770", "OFGP"],
    ["6a0400434d4C", "BCML"],
    ["6a040048533e", "p2sh notification"],
    ["6a04004F5243", "Oracle Data"],
    ["6a0400504642", "BitcoinFiles"],
    ["6a0400504c53", "Simple Ledger Protocol"],
    ["6a04005171C0", "Silico Signing Protocol"],
    ["6a0400544542", "ChainBet"],
    ["6a0400555354", "UniSOT"],
    ["6a0400584350", "Counterparty Cash"],
    ["6a0400626368", "BChan"],
    ["6a04006d7367", "Cashslide"],
    ["6a0400746C6B", "Keyport"],
    ["6a0401010101", "Cash Accounts"],
    ["6a0402446365", "SatoshiDICE"],
    ["6a0404008080", "BCH-DNS"],
    ["6a04054c5638", "TokenGroups"],
    ["6a0408776863", "Wormhole"],
    ["6a22314c74794d45366235416e4d6f70517242504c6b3446474e3855427568784b71726e", "weathersv"],
    ["6a223", "bitcom"]
]

def protocol_mapper(script: str) -> str:
    for prefix, protocol in prefixes:
        if script.startswith(prefix.lower()):
            return protocol
    
    return script[2:8]

if __name__ == "__main__":
    args = parser.parse_args()
    protocol_counter(args)