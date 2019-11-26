from .PipelineABC import Pipeline as Pipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Transformers.CastToFloats import CastToFloats
from ..Transformers.Divider import Divider
from ..Transformers.Subtractor import Subtractor
from ..DataLoaders.CM_API import CM_API

class ETHContractsPipe(Pipe):
    def __init__(self, api_key:str, additional_metrics:[str]=[], start:str=None, end:str=None):
        super().__init__()
        self.api_key = api_key
        self.assets = ['eth']
        self.start = start
        self.end = end
        self.metrics = metrics = [  
            'GasUsedTx',
            'GasUsedTxMean',
            'GasLmtBlk',
            'GasLmtTx', 
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
            'ContBalCnt',
            'ContCnt',
            'ContERC20Cnt',
            'ContERC721Cnt',
            'TxCnt',
            'TxTfrCnt'
        ] + additional_metrics
        
    def implement(self):
        df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.assets, metrics=self.metrics, start=self.start, end=self.end)

        transformers = [
            DateNormalizer(),
            CastToFloats(),
            Divider(column_a='eth.GasUsedTx', column_b='eth.GasLmtBlk', new_column_name='Ethereum Block Fullness %'),
            Divider(column_a='eth.TxCnt', column_b='eth.TxERC20Cnt'),
            Divider(column_a='eth.TxCnt', column_b='eth.TxERC721Cnt'),
            Divider(column_a='eth.TxTfrCnt', column_b='eth.TxTfrERC20Cnt'),
            Divider(column_a='eth.TxTfrCnt', column_b='eth.TxTfrERC721Cnt'),
            Subtractor(new_column_name='eth.NonTokenTransactions', starting_column='eth.TxCnt', subtractor_columns=['eth.TxERC20Cnt', 'eth.TxERC721Cnt']),
            Subtractor(new_column_name='eth.NonTokenContracts', starting_column='eth.ContCnt', subtractor_columns=['eth.ContERC20Cnt', 'eth.ContERC721Cnt'])
        ]

        self.load_data(df=df)
        self.load_transformers(transformers=transformers)
        self.execute_transformers()

        return self.df