import psycopg2
import pandas as pd

from abc import ABC


class ContractsLoader(ABC):
    def __init__(self, host, port):
        super().__init__()
        self.db_string = f"postgresql://postgres@{host}:{port}/postgres-factory-staging"

    def get_contracts(self, asset, contract_type):
        with psycopg2.connect(self.db_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT ENCODE(contract, 'hex'), type
                    FROM contracts_types
                    WHERE asset = %s
                    AND type = %s
                """, (asset, contract_type))
            
                return pd.DataFrame(data=cursor.fetchall(), columns=["contract", "type"])

if __name__ == "__main__":
    loader = ContractsLoader("localhost", 7432)
    print(loader.get_contracts("eth", "ERC20").head())