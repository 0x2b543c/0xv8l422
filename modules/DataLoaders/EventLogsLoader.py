import psycopg2
import pandas as pd

from abc import ABC


class EventLogsLoader(ABC):
    def __init__(self, host, port, database):
        super().__init__()
        self.db_string = f"postgresql://postgres@{host}:{port}/{database}"

    def get_event_logs(self, contract_address):
        query = """
            SELECT DATE_TRUNC('day', '1970-01-01 00:00:00'::timestamp without time zone + block."timestamp"::double precision * '00:00:01'::interval) as date,
            block.number as block_number, 
            encode(block.hash, 'hex') as block_hash, 
            encode(tx.hash, 'hex') as transaction_hash, 
            encode(tx.from, 'hex') as from, 
            encode(tx.to, 'hex') as to, 
            tx.value, 
            tx.gas, 
            encode(tx.input, 'hex') as input, 
            encode(log.address, 'hex') as address, 
            encode(log.data, 'hex') as data, 
            log.topics
            FROM
                ethereum block,
                UNNEST(block.transactions) tx,
                UNNEST(tx.logs) log
            WHERE
                log."address" = E'\\x41A322b28D0fF354040e2CbC676F0320d8c8850d'
            AND
                block.number < 5500000
            AND
                block.number > 5493000
        """
        test_query = """
            SELECT * 
            FROM ethereum block
            WHERE block.number = 5500000
        """
        with psycopg2.connect(self.db_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                print('data', cursor.fetchall())
                return pd.DataFrame(data=cursor.fetchall())

# if __name__ == "__main__":
#     superrare_contract = "0x41A322b28D0fF354040e2CbC676F0320d8c8850d"
#     loader = ContractsLoader("localhost", 5432, "postgres2replica2")
#     print(loader.get_event_logs(contract_address=superrare_contract).head())
