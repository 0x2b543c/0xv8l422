from .DataLoaderABC import DataLoader as DataLoader

class CMDataGroups(DataLoader):
    def __init__(self):
        super().__init__()
    
    def get_asset_group(self, group_name):
        asset_groups = {
            'stablecoins': ['dai', 'gusd', 'pax', 'usdc', 'tusd', 'usdt', 'usdt_eth'],
            'erc-20s': ['ant', 'bat', 'cennz', 'ctxc', 'cvc', 'fun', 'link', 'loom', 'gno', 'gnt', 'icn', 'lrc', 'mana', 'mkr', 'omg', 'pay', 'poly', 'powr', 'ppt', 'qash', 'rep', 'salt', 'sr', 'wtc', 'zrx'],
            'pow-chains': ['bch', 'bsv', 'btc', 'btg', 'dash', 'doge', 'etc', 'eth', 'ltc', 'vtc', 'xmr', 'zec'],
            'btc-forks': ['bch', 'bsv', 'btc','btg'],
            'privacy-coins': ['grin', 'xmr','xvg','zec'],
            'exchange-tokens': ['bnb', 'bnb_mainnet', 'ht', 'knc', 'leo_eos', 'leo_eth', 'zrx']
        }
        return asset_groups[group_name]
    
    def get_metric_group(self, group_name):
        metric_groups = {
            'addresses-w-balance-greater-than-x-usd': ['AdrBalUSD1Cnt', 'AdrBalUSD10Cnt', 'AdrBalUSD100Cnt', 'AdrBalUSD1KCnt', 'AdrBalUSD10KCnt', 'AdrBalUSD100KCnt', 'AdrBalUSD1MCnt', 'AdrBalUSD10MCnt'],
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
            ]
        }
        return metric_groups[group_name]