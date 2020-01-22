from .ReportABC import Report as Rep
from ..Visualizers.LineChartMetricByAssets import LineChartMetricByAssets
from ..Visualizers.LineChartAssetByMetrics import LineChartAssetByMetrics
from ..Visualizers.MarketShareAssetsByMetric import MarketShareAssetsByMetric 
from ..Visualizers.MarketShareMetricsByAsset import MarketShareMetricsByAsset
from ..Visualizers.LineChart import LineChart
from ..Pipelines.NetworkDataPipe import NetworkDataPipe
from ..Transformers.PercentGrowth import PercentGrowth
from ..Transformers.RollingAverage import RollingAverage

class CoinbaseReport(Rep):
    def __init__(self, title:str, api_key:str, assets:[str], start:str=None, end:str=None, growth=False, market_share=False, aggregate:bool=False, aggregated_assets_name:str=None, seven_day_rolling_average:bool=False, log_y_axis:bool=False, y2_axis_columns:[str]=None):
        super().__init__(title=title, api_key=api_key, start=start, end=end)
        self.api_key = api_key
        self.assets = assets 
        self.growth = growth
        self.market_share = market_share
        self.aggregate = aggregate
        self.aggregated_assets_name = aggregated_assets_name
        self.seven_day_rolling_average = seven_day_rolling_average
        self.log_y_axis = log_y_axis
        self.y2_axis_columns = y2_axis_columns

    def implement(self):
        economic_metrics = [
            'TxTfrValAdjUSD',
            'TxTfrCnt',
            'IssContPctAnn',
            'FeeTotUSD',
            'FeeMedUSD',
            'VelActAdj1yr'
        ]

        valuation_metrics = [
            'CapRealUSD',
            'CapMrktCurUSD',
            'CapMVRVCur',
            'PriceUSD',
            'SOPR'
        ]

        usage_metrics = [
            'AdrActCnt',
            'TxCnt',
            'BlkSizeMeanByte',
            'AdrBalUSD10Cnt',
            'AdrBalUSD1MCnt'
        ]

        security_metrics = [
            'HashRate',
            'DiffMean',
            'RevUSD'
        ]

        sply_held_by_exchanges_metrics = [
            'SplyBFXNtv',
            'SplyBMXNtv',
            'SplyBNBNtv',
            'SplyBSPNtv',
            'SplyBTXNtv',
            'SplyGEMNtv',
            'SplyHUONtv',
            'SplyKRKNtv',
            'SplyPOLNtv'
        ]

        active_supply_metrics = ['SplyAct30d', 'SplyAct180d', 'SplyAct1yr', 'SplyAct2yr', 'SplyAct3yr', 'SplyAct4yr', 'SplyAct5yr']

        addresses_with_balance_greater_than_X_ntv_metrics = ['AdrBalNtv0.1Cnt', 'AdrBalNtv1Cnt', 'AdrBalNtv10Cnt', 'AdrBalNtv100Cnt', 'AdrBalNtv1KCnt']

        addresses_with_balance_greater_than_X_usd_metrics = ['AdrBalUSD1Cnt', 'AdrBalUSD10Cnt', 'AdrBalUSD100Cnt', 'AdrBalUSD1KCnt', 'AdrBalUSD10KCnt', 'AdrBalUSD100KCnt', 'AdrBalUSD1MCnt', 'AdrBalUSD10MCnt']

        addresses_with_balance_greater_than_1_in_X_ntv_metrics = ['AdrBal1in100KCnt', 'AdrBal1in1MCnt', 'AdrBal1in10MCnt', 'AdrBal1in100MCnt', 'AdrBal1in1BCnt']

        all_metrics = economic_metrics + valuation_metrics + usage_metrics + security_metrics + active_supply_metrics + addresses_with_balance_greater_than_X_ntv_metrics + addresses_with_balance_greater_than_1_in_X_ntv_metrics + addresses_with_balance_greater_than_X_usd_metrics + sply_held_by_exchanges_metrics

        all_metrics = list(set(all_metrics))

        df = NetworkDataPipe(api_key=self.api_key, assets=self.assets, metrics=all_metrics, start=self.start, aggregate=self.aggregate, aggregated_assets_name=self.aggregated_assets_name).run()
        
        if self.growth == True:
            df= PercentGrowth().transform(df)
        if self.seven_day_rolling_average == True:
            df= RollingAverage(number_of_days=7).transform(df)

        _chart = MarketShareAssetsByMetric if self.market_share == True else LineChartMetricByAssets
        _distribution_chart = MarketShareMetricsByAsset if self.market_share == True else LineChartAssetByMetrics


        self.assets = self.assets if self.aggregate == False else [self.aggregated_assets_name]

        valuation_visuals = [
            _chart(df=df, title=metric, metric=metric, assets=self.assets, section='valuation', y2_axis_columns=self.y2_axis_columns).run() for metric in valuation_metrics
        ]

        economic_visuals = [
            _chart(df=df, title=metric, metric=metric, assets=self.assets, section='economics', y2_axis_columns=self.y2_axis_columns).run() for metric in economic_metrics
        ]

        usage_visuals = [
            _chart(df=df, title=metric, metric=metric, assets=self.assets, section='usage', y2_axis_columns=self.y2_axis_columns).run() for metric in usage_metrics
        ]

        security_visuals = [
            _chart(df=df, title=metric, metric=metric, assets=self.assets, section='security', y2_axis_columns=self.y2_axis_columns).run() for metric in security_metrics
        ]

        active_supply_visuals = [
            _distribution_chart(df=df, title=f'{asset} Active Supply', metrics=active_supply_metrics, asset=asset, section='active-supply', filled_area=True).run() for asset in self.assets
        ]


        addresses_with_balance_greater_than_1_in_X_ntv_visuals = [
            _distribution_chart(df=df, title=f'{asset} Addresses W/ Balance >1 in X (Native Units)', metrics=addresses_with_balance_greater_than_1_in_X_ntv_metrics, asset=asset, section='token-distributions', filled_area=True).run() for asset in self.assets
        ]

        addresses_with_balance_greater_than_X_ntv_visuals = [
            _distribution_chart(df=df, title=f'{asset} Addresses W/ Balance > X (Native Units)', metrics=addresses_with_balance_greater_than_X_ntv_metrics, asset=asset, section='token-distributions', filled_area=True).run() for asset in self.assets
        ]

        addresses_with_balance_greater_than_X_usd_visuals = [
            _distribution_chart(df=df, title=f'{asset} Addresses W/ Balance > X (USD)', metrics=addresses_with_balance_greater_than_X_usd_metrics, asset=asset, section='token-distributions', filled_area=True).run() for asset in self.assets
        ]

        btc_held_by_exchanges_visuals = [
            _distribution_chart(df=df, title=f'{asset} Held By Exchanges, % Share of Total, (Native Units)', metrics=sply_held_by_exchanges_metrics, asset=asset, section='exchange-flows', filled_area=True).run() for asset in self.assets
        ]

        # exchange_flows = [
        #     _distribution_chart(df=df, title=f'{asset} Held By Exchanges, % Share of Total, (Native Units)', metrics=sply_held_by_exchanges_metrics, asset=asset, section='exchange-flows', filled_area=True).run() for asset in self.assets
        # ]

        sopr_visuals = [
            LineChart(df=df, title=f'{asset} SOPR', y_columns=[f'{asset}.SOPR'], y2_axis_columns=[f'{asset}.PriceUSD'], section='valuation').run() for asset in self.assets
        ]

        all_visuals = valuation_visuals + economic_visuals + usage_visuals + security_visuals + active_supply_visuals + addresses_with_balance_greater_than_1_in_X_ntv_visuals+ addresses_with_balance_greater_than_X_ntv_visuals + addresses_with_balance_greater_than_X_usd_visuals + btc_held_by_exchanges_visuals + sopr_visuals

        if self.log_y_axis == True:
            for visual in all_visuals:
                visual.fig.update_yaxes(type="log")

        self.load_visual(all_visuals)
        self.dfs.append(df)
        if self.growth == True:
            self.format_y_axis_as_percent()
        
        
