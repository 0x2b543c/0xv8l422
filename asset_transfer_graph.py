import psycopg2
import argparse
import sys
import networkx as nx
import itertools
from collections import defaultdict

from datetime import datetime, timedelta
from utils import valid_date
from transfers import get_transfers

parser = argparse.ArgumentParser(description='Returns a transfer value weighted graph of asset addresses')
parser.add_argument('--host', type=str, required=True)
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--start', type=valid_date, required=True, help="YYYY-MM-DD")
parser.add_argument('--end', type=valid_date, required=True, help="YYYY-MM-DD")
parser.add_argument('--asset', type=str, required=True)
parser.add_argument('--threshold', type=float, required=True, help="Edge weight threshold")
parser.add_argument('--output', type=str, required=True, help="output file (GEXF)")

if __name__ == "__main__":
    args = parser.parse_args()

    current_date = args.start

    G = nx.MultiDiGraph()

    hot_wallets = {
        "1Po1oWkD2LmodfkBYiAktwh76vkF93LKnh": "Poloniex",
        "1KYiKJEfdJtap9QX2v9BXJMpz2SfU4pgZw": "Bitfinex",
        "1DUb2YYbQA1jjaNYzVXLZ7ZioEhLXtbUru": "Bittrex",
        "1FoWyxwPXuj4C6abqwhjDWdz6D4PZgYRjA": "Binance",
        "1HckjUpRGcrrRAtFaaCAUaGjsPx9oYmLaZ": "Huobi",
        "1ApkXfxWgJ5CBHzrogVSKz23umMZ32wvNA": "OKex",
        "1gJ4FX7n4Udk1LVUSnutAgznyG9JZdQEU": "Liqui.io",
        "15Fkf4K6z6XQXr1xoNBDDTaR9GBMX6JdyF": "HitBTC",
        "3GyeFJmQynJWd8DeACm4cdEnZcckAtrfcN": "Kraken",
        "168o1kqNquEJeR9vosUB5fw4eAwcVAgh8P": "Huobi"     
    }
    
    edges = {}

    total_volume = 0
    arb_volume = 0

    addr_to_recipients = defaultdict(set)

    def label_node(addr: str) -> str:
        if addr in hot_wallets:
            return hot_wallets[addr]

        recipients = list(addr_to_recipients[addr])
        if len(recipients) == 1 and recipients[0] in hot_wallets:
            exchange = hot_wallets[recipients[0]]
            return "Deposit {} - {}".format(exchange, addr[:5])

        return addr

    with psycopg2.connect("postgresql://postgres@{}:{}/postgres-factory-production".format(args.host, args.port)) as conn:
        while current_date <= args.end:
            transfers = get_transfers(conn, args.asset, current_date)
            for t in transfers:
                if t.transfer_type == "NORMAL":
                    addr_to_recipients[t.source].add(t.destination)

                    total_volume += float(t.value)
                    if t.source not in edges:
                        edges[t.source] = {}
                    if t.destination not in edges[t.source]:
                        edges[t.source][t.destination] = 0.0

                    edges[t.source][t.destination] += float(t.value)
                    
            print("{}".format(current_date))
            current_date += timedelta(days=1)

    # Get nodes involved in edges over threshold
    for source in edges:
        for destination in edges[source]:
            weight = edges[source][destination]
            if weight >= args.threshold:
                G.add_edge(source, destination, weight=weight)


    # relabel nodes to identify exchanges/deposit addresses
    labels = {n: label_node(n) for n in G.nodes}
    G2 = nx.relabel_nodes(G, labels)
    nx.write_gexf(G2, args.output)