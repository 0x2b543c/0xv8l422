from .DataLoaderABC import DataLoader as DataLoader

class CMDataGroups(DataLoader):
    def __init__(self):
        super().__init__()
        self.asset_groups = {
            'stablecoins': ['dai', 'gusd', 'pax', 'usdc', 'tusd', 'usdt', 'usdt_eth', 'usdt_trx'],
            'tether': ['usdt', 'usdt_eth', 'usdt_trx'],
            'non-tether-stablecoins': ['dai', 'gusd', 'pax', 'usdc', 'tusd'],
            'erc-20s': ['ant', 'bat', 'cennz', 'ctxc', 'cvc', 'fun', 'link', 'loom', 'gno', 'gnt', 'icn', 'lrc', 'mana', 'mkr', 'omg', 'pay', 'poly', 'powr', 'ppt', 'qash', 'rep', 'salt', 'sr', 'wtc', 'zrx'],
            'pow-chains': ['bch', 'bsv', 'btc', 'btg', 'dash', 'doge', 'etc', 'eth', 'ltc', 'vtc', 'xmr', 'zec'],
            'btc-forks': ['bch', 'bsv', 'btc','btg'],
            'privacy-coins': ['grin', 'xmr','xvg','zec'],
            'exchange-tokens': ['bnb', 'bnb_mainnet', 'ht', 'knc', 'leo_eos', 'leo_eth', 'zrx'],
            'network-data-sample': [
                'btc',
                'xrp',
                'eth',
                'bch',
                'ltc',
                'xlm',
                'xtz',
                'bsv',
                'ada',
                'zec',
                'link',
                'dcr',
                'mkr',
                'bat',
                'usdt',
                'usdt_eth',
                'pax',
                'usdc'
            ]
        }
        self.metric_groups = {
            'addresses-with-balance-greater-than-x-usd': [
                'AdrBalUSD1Cnt', 'AdrBalUSD10Cnt', 'AdrBalUSD100Cnt', 'AdrBalUSD1KCnt', 'AdrBalUSD10KCnt', 'AdrBalUSD100KCnt', 'AdrBalUSD1MCnt'
                ],
            'addresses-with-balance-greater-than-x-ntv': [
                'AdrBalNtv0.001Cnt', 'AdrBalNtv0.01Cnt', 'AdrBalNtv0.1Cnt', 'AdrBalNtv1Cnt', 'AdrBalNtv10Cnt', 'AdrBalNtv100Cnt', 'AdrBalNtv1KCnt', 'AdrBalNtv10KCnt', 'AdrBalNtv100KCnt'
                ],
            'addresses-with-balance-greater-than-1-in-x': [
                'AdrBal1in1KCnt', 'AdrBal1in10KCnt', 'AdrBal1in100KCnt', 'AdrBal1in1MCnt', 'AdrBal1in10MCnt', 'AdrBal1in100MCnt', 'AdrBal1in1BCnt', 'AdrBal1in10BCnt'
                ],
            'active-supply': [
                'SplyAct1d', 'SplyAct7d', 'SplyAct30d', 'SplyAct90d', 'SplyAct180d', 'SplyAct1yr', 'SplyAct2yr', 'SplyAct3yr', 'SplyAct4yr', 'SplyAct5yr'
                ],
            'supply-in-address-with-balance-greater-than-x-usd': [
                'SplyAdrBalUSD1', 'SplyAdrBalUSD10', 'SplyAdrBalUSD100', 'SplyAdrBalUSD1K', 'SplyAdrBalUSD10K', 'SplyAdrBalUSD100K', 'SplyAdrBalUSD1M', 'SplyAdrBalUSD10M'
                ], 
            'supply-in-address-with-balance-greater-than-x-ntv': [
                'SplyAdrBalNtv0.001', 'SplyAdrBalNtv0.01', 'SplyAdrBalNtv0.1', 'SplyAdrBalNtv1', 'SplyAdrBalNtv10', 'SplyAdrBalNtv100', 'SplyAdrBalNtv1K','SplyAdrBalNtv10K', 'SplyAdrBalNtv100K', 'SplyAdrBalNtv1M'
                ],  
            'supply-in-address-with-balance-greater-than-1-in-x': [
                'SplyAdrBal1in1K', 'SplyAdrBal1in10K', 'SplyAdrBal1in100K', 'SplyAdrBal1in1M', 'SplyAdrBal1in10M', 'SplyAdrBal1in100M', 'SplyAdrBal1in1B', 'SplyAdrBal1in10B'
                ],
            'valuation': [
                'CapRealUSD',
                'CapMrktCurUSD',
                'CapMVRVCur',
                'VtyDayRet30d',
                'PriceUSD'  
            ],
            'usage': [
                'AdrActCnt',
                'AdrBalUSD10Cnt',
                'AdrBalUSD1MCnt',
                'BlkSizeByte'
            ],
            'security': [
                    'HashRate',
                    'DiffMean',
                    'FeeTotUSD',
                    'FeeRevPct',
                    'RevUSD',
                    'RevAllTimeUSD'
            ],
            'economics': [
                    'TxCnt',
                    'TxTfrCnt',
                    'TxTfrValAdjUSD',
                    'IssContPctAnn',
                    'FeeMedUSD',
                    'VelActAdj1yr',
                    'TxTfrValAdjByte'
            ],
            'btc-specific': [
                'TxOpRetCnt',
                'UTXOCnt',
                'SOPR',
            ],
            'eth-specific': [
                'ContBalCnt',
                'ContCnt',
                'ContERC20Cnt',
                'ContERC721Cnt',
                'GasLmtBlk',
                'GasLmtBlkMean',
                'GasLmtTx',
                'GasLmtTxMean',
                'GasUsedTx',
                'GasUsedTxMean',
                'TxContCallCnt',
                'TxContCallSuccCnt',
                'TxContCnt',
                'TxContCreatCnt',
                'TxContDestCnt',
                'TxERC20Cnt',
                'TxERC721Cnt',
                'TxTfrERC20Cnt',
                'TxTfrERC721Cnt',
                'TxTfrTknCnt',
                'TxTknCnt',
                'TxTfrValContCallNtv',
                'TxTfrValContCallUSD'
            ]
        } 
    
    def get_asset_group(self, group_name):
        return self.asset_groups[group_name]
    
    def get_metric_group(self, group_name):
        return self.metric_groups[group_name]