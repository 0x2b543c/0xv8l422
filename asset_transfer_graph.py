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

    hot_wallets = {
        "1Po1oWkD2LmodfkBYiAktwh76vkF93LKnh": "Poloniex",
        "1Co1dhYDeF76DQyEyj4B5JdXF9J7TtfWWE": "Poloniex",

        "1KYiKJEfdJtap9QX2v9BXJMpz2SfU4pgZw": "Bitfinex",
        "13TMLJdKgCnQLiv4Bx65DqpKvgnC2pdLLC": "Bitfinex",

        "1DUb2YYbQA1jjaNYzVXLZ7ZioEhLXtbUru": "Bittrex",

        "1FoWyxwPXuj4C6abqwhjDWdz6D4PZgYRjA": "Binance",
        "12uhUkxpwkD2LGzKHUywoknoJ3fC9vev1x": "Binance",
        "1H9HSzuzsV3R6fVHp9xPhVF9Z2mn3Lu3rP": "Binance",

        "1ApkXfxWgJ5CBHzrogVSKz23umMZ32wvNA": "OKex",
        "37Tm3Qz8Zw2VJrheUUhArDAoq58S6YrS3g": "OKex",

        "1gJ4FX7n4Udk1LVUSnutAgznyG9JZdQEU": "Liqui.io",
        "1DGUWy6N6iHTpussbSP8XrK96tZgDboiWK": "Liqui.io",

        "15Fkf4K6z6XQXr1xoNBDDTaR9GBMX6JdyF": "HitBTC",
        "115E3baxJZsJHeTay1jvUh3nSTHBJhkskc": "HitBTC", # https://twitter.com/rolflobker/status/946296202341027850

        "3GyeFJmQynJWd8DeACm4cdEnZcckAtrfcN": "Kraken",
        "3NmqEssZvQomHbJFi72Hg3sEwBh6pSM6Zk": "Kraken",

        "168o1kqNquEJeR9vosUB5fw4eAwcVAgh8P": "Huobi",
        "1LAnF8h3qMGx3TSwNUHVneBZUEpwE4gu3D": "Huobi",
        "1HckjUpRGcrrRAtFaaCAUaGjsPx9oYmLaZ": "Huobi",
        "35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP": "Huobi",

        "16Xp1ddLctkYEhBdgnUCv8kFnuxEiySES5": "Cryptopia?", # http://www.blockspur.com/tether/addresses/16Xp1ddLctkYEhBdgnUCv8kFnuxEiySES5

        "1DcKsGnjpD38bfj6RMxz945YwohZUTVLby": "Gate.io",

        "3BbDtxBSjgfTRxaBUgR2JACWRukLKtZdiQ": "Treasury",
        "1NTMakcgVwQpMdGxRQnFKyb3G1FAJysSfz": "Treasury",

        "1ENVTkd9f5KUkvcKSutiJwdBVPgaPh6ihT": "Entity A",
        "1Gc3biG5hsHAoj4ZNAtnT4sCBbtF9sKEEL": "Entity B",
        "16bUGjvunVp7LqygLHrTvHyvbvfeuRCWAh": "Entity C",
        "17JRuZyQoA7uyZarmDGmSGtvksYcYLBhrX": "Entity D",
        "14i8cEbkAeQhx7XSTijk4noFAGtfSGndsk": "Entity E",
        "12aGp6kiy6pmv2pVYfAHq8BuurK78iCMXn": "Entity F",

        # ETH data
        "e853c56864a2ebe4576a807d26fdc4a0ada51919": "Kraken",
        "4e9ce36e442e55ecd9025b9a6e0d88485d628a67": "Binance",
        "742d35cc6634c0532925a3b844bc454e4438f44e": "Bitfinex",
        "53d284357ec70ce289d6d64134dfac8e511c8a3d": "Kraken",
        "66f820a414680b5bcda5eeca5dea238543f42054": "Bittrex",
        "61edcdf5bb737adffe5043706e7c5bb1f1a56eea": "Gemini",
        "dc76cd25977e0a5ae17155770273ad58648900d3": "Huobi",
        "fbf2173154f7625713be22e0504404ebfe021eae": "Poloniex",
        "6f803466bcd17f44fa18975bf7c509ba64bf3825": "Poloniex",
        "ead6be34ce315940264519f250d8160f369fa5cd": "Poloniex",
        "b8cf411b956b3f9013c1d0ac8c909b086218207c": "Remitano",
        "2819c144d5946404c0516b6f817a960db37d4929": "Remitano",
        "120a270bbc009644e35f0bb6ab13f95b8199c4ad": "ShapeShift",
        "9e6316f44baeeee5d41a1070516cc5fa47baf227": "ShapeShift",
        "70faa28a6b8d6829a4b1e649d26ec9a2a39ba413": "ShapeShift",
        "563b377a956c80d77a7c613a9343699ad6123911": "ShapeShift",
        "d3273eba07248020bf98a8b560ec1576a612102f": "ShapeShift",
        "3b0bc51ab9de1e5b7b6e34e5b960285805c41736": "ShapeShift",
        "eed16856d551569d134530ee3967ec79995e2051": "ShapeShift",
        "3613ef1125a078ef96ffc898c4ec28d73c5b8c52": "Tidex",
        "0a73573cf2903d2d8305b1ecb9e9730186a312ae": "Tidex",
        "b2cc3cdd53fc9a1aeaf3a68edeba2736238ddc5d": "TopBTC",
        "1119aaefb02bf12b84d28a5d8ea48ec3c90ef1db": "Trade.io",
        "2f1233ec3a4930fd95874291db7da9e90dfb2f03": "Uex",
        "390de26d772d2e2005c6d1d24afc902bae37a4bb": "Upbit",
        "ba826fec90cefdf6706858e5fbafcb27a290fbe0": "Upbit",
        "5e032243d507c743b061ef021e2ec7fcc6d3ab89": "Upbit",
        "d94c9ff168dc6aebf9b6cc86deff54f3fb0afc33": "Yunbi",
        "42da8a05cb7ed9a43572b5ba1b8f82a0a6e263dc": "Yunbi",
        "700f6912e5753e91ea3fae877a2374a2db1245d7": "Yunbi",
        "60d0cc2ae15859f69bf74dadb8ae3bd58434976b": "ZB.com",
        "521db06bf657ed1d6c98553a70319a8ddbac75a3": "CREX24",
        "5baeac0a0417a05733884852aa068b706967e790": "Cryptopia",
        "2984581ece53a4390d1f568673cf693139c97049": "Cryptopia",
        "e17ee7b3c676701c66b395a35f0df4c2276a344e": "DigiFinex",
        "915d7915f2b469bb654a7d903a5d4417cb8ea7df": "FCoin",
        "7793cd85c11a924478d358d49b05b37e91b5810f": "Gate.io",
        "9f5ca0012b9b72e8f3db57092a6f26bf4f13dc69": "GBX",
        "6fc82a5fe25a5cdb58bc74600a40a69c065263f8": "Gemini",
        "9c67e141c0472115aa1b98bd0088418be68fd249": "HitBtc",
        "59a5208b32e627891c389ebafc644145224006e8": "HitBtc",
        "a12431d0b9db640034b0cdfceef9cce161e62be4": "HitBtc",
        "274f3c32c90517975e29dfc209a23f315c1e5fc7": "Hotbit",
        "8533a0bd9310eb63e7cc8e1116c18a3d67b1976a": "Hotbit",
        "ab5c66752a9e8167967685f1450532fb96d5d24f": "Huobi",
        "e93381fb4c4f14bda253907b18fad305d799241a": "Huobi",
        "fa4b5be3f2f84f56703c42eb22142744e95a2c58": "Huobi",
        "46705dfff24256421a05d056c29e81bdc09723b8": "Huobi",
        "1b93129f05cc2e840135aab154223c75097b69bf": "Huobi",
        "eb6d43fe241fb2320b5a3c9be9cdfd4dd8226451": "Huobi",
        "956e0dbecc0e873d34a5e39b25f364b2ca036730": "Huobi",
        "6748f50f686bfbca6fe8ad62b22228b87f31ff2b": "Huobi",
        "fdb16996831753d5331ff813c29a93c76834a0ad": "Huobi",
        "eee28d484628d41a82d01e21d12e2e78d69920da": "Huobi",
        "5c985e89dde482efe97ea9f1950ad149eb73829b": "Huobi",
        "adb2b42f6bd96f5c65920b9ac88619dce4166f94": "Huobi",
        "a8660c8ffd6d578f657b72c0c811284aef0b735e": "Huobi",
        "1062a747393198f70f71ec65a582423dba7e5ab3": "Huobi",
        "fa52274dd61e1643d2205169732f29114bc240b3": "Kraken",
        "e8a0e282e6a3e8023465accd47fae39dd5db010b": "Kryptono",
        "629a7144235259336ea2694167f3c8b856edd7dc": "Kryptono",
        "30b71d015f60e2f959743038ce0aaec9b4c1ea44": "Kryptono",
        "2b5634c42055806a59e9107ed44d43c426e58258": "KuCoin",
        "689c56aef474df92d44a1b70850f808488f9769c": "KuCoin",
        "0861fca546225fbf8806986d211c8398f7457734": "LAToken",
        "7891b20c690605f4e370d6944c8a5dbfac5a451c": "LAToken",
        "8271b2e8cbe29396e9563229030c89679b9470db": "Liqui.io",
        "5e575279bf9f4acf0a130c186861454247394c06": "Liqui.io",
        "edbb72e6b3cf66a792bff7faac5ea769fe810517": "Liquid",
        "243bec9256c9a3469da22103891465b47583d9f1": "Livecoin.net",
        "e03c23519e18d64f144d2800e30e81b0065c48b5": "Mercatox",
        "ae7006588d03bd15d6954e3084a7e644596bc251": "NEXBIT Pro",
        "236f9f97e0e62388479bf9e5ba4889e46b0273c3": "Okex",
        "aeec6f5aca72f3a005af1b3420ab8c8c7009bac8": "OTCBTC",
        "bd8ef191caa1571e8ad4619ae894e07a75de0c35": "Paribu",
        "2bb97b6cf6ffe53576032c11711d59bd056830ee": "Paribu",
        "d4dcd2459bb78d7a645aa7e196857d421b10d93f": "Peatio",
        "209c4784ab1e8183cf58ca33cb740efbf3fc18ef": "Poloniex",
        "b794f5ea0ba39494ce839613fffba74279579268": "Poloniex",
        "a910f92acdaf488fa6ef02174fb86208ad7722ba": "Poloniex",
        "aa9fa73dfe17ecaa2c89b39f0bb2779613c5fc3b": "Poloniex",
        "2fa2bc2ce6a4f92952921a4caa46b3727d24a1ec": "Poloniex",
        "31a2feb9b5d3b5f4e76c71d6c92fc46ebb3cb1c1": "Poloniex",
        "6b71834d65c5c4d8ed158d54b47e6ea4ff4e5437": "Poloniex",
        "48d466b7c0d32b61e8a82cd2bcf060f7c3f966df": "Poloniex",
        "0536806df512d6cdde913cf95c9886f65b1d3462": "Poloniex",
        "8d451ae5ee8f557a9ce7a9d7be8a8cb40002d5cb": "Poloniex",
        "bd2ec7c608a06fe975dbdca729e84dedb34ecc21": "Poloniex",
        "c0e30823e5e628df8bc9bf2636a347e1512f0ecb": "Poloniex",
        "65f9b2e4d7aaeb40ffea8c6f5844d5ad7da257e0": "Poloniex",
        "36b01066b7fa4a0fdb2968ea0256c848e9135674": "Poloniex",
        "ab11204cfeaccffa63c2d23aef2ea9accdb0a0d5": "Poloniex",
        "6795cf8eb25585eadc356ae32ac6641016c550f2": "Poloniex",
        "267be1c1d684f78cb4f6a176c4911b741e4ffdc0": "Kraken",
        "6cc5f688a315f3dc28a7781717a9a798a59fda7b": "Okex",
        "fbb1b73c4f0bda4f67dca266ce6ef42f520fbb98": "Bittrex",
        "0a869d79a7052c7f1b55a8ebabbea3420f0d1e13": "Kraken",
        "4fdd5eb2fb260149a3903859043e962ab89d8ed4": "Bitfinex",
        "32be343b94f860124dc4fee278fdcbd38c102d88": "Poloniex",
        "d24400ae8bfebb18ca49be86258a3c749cf46853": "Gemini",
        "1c4b70a3968436b9a0a9cf5205c787eb81bb558c": "Gate.io",
        "1342a001544b8b7ae4a5d374e33114c66d78bd5f": "Gatecoin",
        "d4914762f9bd566bd0882b71af5439c0476d2ff6": "Gatecoin",
        "f5bec430576ff1b82e44ddb5a1c93f6f9d0884f3": "YoBit",
        "876eabf441b2ee5b5b0554fd502a8e0600950cfa": "Bitfinex",
        "0d0707963952f2fba59dd06f2b425ace40b492fe": "Gate.io",
        "3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be": "Binance",
        "04786aada9deea2150deab7b3b8911c309f5ed90": "Gatecoin",
        "2910543af39aba0cd09dbb2d50200b3e800a63d2": "Kraken",
        "eec606a66edb6f497662ea31b5eb1610da87ab5f": "Huobi",
        "05f51aab068caa6ab7eeb672f88c180f67f17ec7": "ABCC",
        "7a10ec7d68a048bdae36a70e93532d31423170fa": "Bgogo",
        "ce1bf8e51f8b39e51c6184e059786d1c0eaf360f": "Bgogo",
        "f73c3c65bde10bf26c2e1763104e609a41702efe": "Bibox",
        "a30d8157911ef23c46c0eb71889efe6a648a41f7": "BigONE",
        "f7793d27a1b76cdf14db7c83e82c772cf7c92910": "Bilaxy",
        "d551234ae421e3bcba99a0da6d736074f22192ff": "Binance",
        "564286362092d8e7936f0549571a803b203aaced": "Binance",
        "0681d8db095565fe8a346fa0277bffde9c0edbbf": "Binance",
        "fe9e8709d3215310075d67e3ed32a380ccf451c8": "Binance",
        "7c49e1c0e33f3efb57d64b7690fa287c8d15b90a": "Bit2C",
        "df5021a4c1401f1125cd347e394d977630e17cf7": "Bitbox",
        "1151314c646ce4e0efd76d1af4760ae66a9fe30f": "Bitfinex",
        "7727e5113d1d161373623e5f49fd568b4f543a9e": "Bitfinex",
        "8fa8af91c675452200e49b4683a33ca2e1a34e42": "Bithumb",
        "3052cd6bf951449a984fe4b5a38b46aef9455c8e": "Bithumb",
        "3fbe1f8fc5ddb27d428aa60f661eaaab0d2000ce": "Bithumb",
        "e79eef9b9388a4ff70ed7ec5bccd5b928ebb8bd1": "BitMart",
        "03bdf69b1322d623836afbd27679a1c0afa067e9": "Bitmax",
        "4b1a99467a284cc690e3237bc69105956816f762": "Bitmax",
        "e94b04a0fed112f3664e45adb2b8915693dd5ff3": "Bittrex",
        "aa90b4aae74cee41e004bc45e45a427406c4dcae": "BitUN.io",
        "f8d04a720520d0bcbc722b1d21ca194aa22699f2": "BitUN.io",
        "fb9f7f41319157ac5c5dccae308a63a4337ad5d9": "Bity.com",
        "72bcfa6932feacd91cb2ea44b0731ed8ae04d0d3": "Cashierest",
        "fd648cc72f1b4e71cbdda7a0a91fe34d32abd656": "ChainX",
        "96fc4553a00c117c5b0bed950dd625d1c16dc894": "Changelly",
        "8958618332df62af93053cb9c535e26462c959b0": "Cobinhood",
        "b726da4fbdc3e4dbda97bb20998cf899b0e727e0": "Cobinhood",
        "9539e0b14021a43cde41d9d45dc34969be9c7cb0": "CoinBene",
        "33683b94334eebc9bd3ea85ddbda4a86fb461405": "CoinBene",
        "b6ba1931e4e74fd080587688f6db10e830f810d5": "Coindelta",
        "b9ee1e551f538a464e8f8c41e9904498505b49b0": "Coinex",
        "4b01721f0244e7c5b5f63c20942850e447f5a5ee": "CoinExchange.io",
        "1d1bd550197c7c0787b9ad0aea9c1cca66ee0e90": "CoinHako",
        "0d6b5a54f940bf3d52e438cab785981aaefdf40c": "COSS.io",
        "d1560b3984b7481cd9a8f40435a53c860187174d": "COSS.io",
        "50bee102a94eb2b1c0aa716a811de35a694e3387": "Poloniex",
        "d532ebeb6ab531d230b6ad18c93e265ff0101dea": "Poloniex",
        "d329c11106d696cf5165265a00decfaa0f0878f1": "Poloniex",
        "b8a2626a015b86d1cf1f8445de0b0c6e65a7afb8": "Poloniex",
        "25b7231d3a8013ef4deb454e5c561a8b49149390": "Poloniex",
        "ef05afdc6fe371cf23b34ab5b8e05775b369bf4a": "Poloniex",
        "54fbd667181db44a28a96b364f294f82f1b0827b": "Poloniex",
        "b7e698183c6735484bcef276ea26125b57846d2c": "Poloniex",
        "03f35f53a2598f9a1c8a452398d08429be70b7fc": "Poloniex",
        "3e962c8bce3c7a7bfbc3ca7a0018e158692ee095": "Poloniex",
        "59cb48d7a44c3eb402f259afa697f830377cbfa4": "Poloniex",
        "92384e84213fad1105e6da1df403aee7ffedfc84": "Poloniex",
        "b1ea6eef811d8fa08650045b8ed8c11aca8f5996": "Poloniex",
        "ae80f9fa64e2330f5de5bd64061285c71c041ed0": "Poloniex",
        "de30e7c5855ed92ace9160deaa331b50f2e6fdbf": "Poloniex",
        "534af382c275aa19dc095bf50c80c8717c86daca": "Poloniex",
        "fa4c4df1a902a70bbd1593c13cac9e8e6c26c566": "Poloniex",
        "ced1bc4b58b19f6f4b90557b0bda0ad328f7e4bb": "Poloniex",
        "6b77702fcb3aae49174b8d1d6064a7cb2a1b3e59": "Poloniex",
        "cff8b7f3ce9542b27e8b938a05179a7f18dbd74e": "Poloniex",
        "9fb01a2584aac5aae3fab1ed25f86c5269b32999": "GGBTC.com",
        "030e37ddd7df1b43db172b23916d523f1599c6cb": "Binance",
        "be0eb53f46cd790cd13851d5eff43d12404d33e8": "Binance",
        "1522900b6dafac587d499a862861c0869be6e428": "Bitstamp",
        "fca70e67b3f93f679992cd36323eeb5a5370c8e4": "Bitstamp",

        "05ee546c1a62f90d7acbffd6d846c9c54c7cf94c": "Gate.io",
        "c6cde7c39eb2f0f0095f41570af89efc2c1ea828": "Treasury",
        "5754284f345afc66a98fbb0a0afe71e0f007b949": "Treasury",
        "c97a4ed29f03fd549c4ae79086673523122d2bc5": "ZB.com",
        "d9811e8b7c42418c71dabfe63b9cc17f8db1a6eb": "BKEX",
        "ff3c260f2391a5a936df3b693b2590045ce62d62": "HotBit?",
        "0211f3cedbef3143223d3acf0e589747933e8527": "MXC?",
        "6efb20f61b80f6a7ebe7a107bace58288a51fb34": "Bikicoin?"
    }
    
    edges = {}

    addr_to_recipients = defaultdict(set)

    _labels = {}

    def label_node(addr: str) -> str:
        if addr in _labels:
            return _labels[addr]

        if addr in hot_wallets:
            return hot_wallets[addr]

        recipients = list(addr_to_recipients[addr])

        # All recipients belong to a single entity? it's a deposit address
        if all(r in hot_wallets for r in recipients) and len({hot_wallets[r] for r in recipients}) == 1:
            exchange = hot_wallets[recipients[0]]
            _labels[addr] = exchange
            return exchange

        _labels[addr] = None
        return None

    with psycopg2.connect("postgresql://postgres@{}:{}/postgres-factory-production".format(args.host, args.port)) as conn:
        while current_date <= args.end:
            transfers = get_transfers(conn, args.asset, current_date)
            for t in transfers:
                if t.transfer_type == "NORMAL":
                    addr_to_recipients[t.source].add(t.destination)

                    if t.source not in edges:
                        edges[t.source] = {}
                    if t.destination not in edges[t.source]:
                        edges[t.source][t.destination] = 0.0

                    edges[t.source][t.destination] += float(t.value)
                    
            print("{}".format(current_date))
            current_date += timedelta(days=1)

    # Now that we have all the info, we compute the graph over entities instead of addresses
    entity_edges = {}

    for source in edges:
        source_entity = label_node(source)

        for destination in edges[source]:
            destination_entity = label_node(destination)
            if source_entity != destination_entity and source_entity is not None and destination_entity is not None:
                if source_entity not in entity_edges:
                    entity_edges[source_entity] = {}
                if destination_entity not in entity_edges[source_entity]:
                    entity_edges[source_entity][destination_entity] = 0.0

                entity_edges[source_entity][destination_entity] += edges[source][destination]


    G = nx.MultiDiGraph()

    # Now we build the graph proper
    for source in entity_edges:
        for destination in entity_edges[source]:
            weight = entity_edges[source][destination]
            if weight >= args.threshold:
                G.add_edge(source, destination, weight=weight)

    nx.write_gexf(G, args.output)