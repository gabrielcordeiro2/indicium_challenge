from sqlalchemy import create_engine, text
from base_logger import BaseLogger
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import sys
import os


class StepTwoQueryOrders(BaseLogger):
    def __init__(self):
        load_dotenv()
        self.__host = os.getenv("DBFINAL_HOST")
        self.__user_db = os.getenv("DBFINAL_USR")
        self.__password_db =  os.getenv("DBFINAL_PWD")
        self.__database_name = os.getenv("DBFINAL_DATABASE")
        self.__port = os.getenv("DBFINAL_PORT")
        self.__engine = create_engine(f'postgresql://{self.__user_db}:{self.__password_db}@{self.__host}:{self.__port}/{self.__database_name}')
        self.logger = self.setup_logger("STEPTWO:QUERYRESULTS")
        self.order_details_path = 'local_storage/order_details/'
    
    def query_results(self):
        with open("data/query_orders.sql", "r") as sql_file:
            query = sql_file.read()

        with self.__engine.connect() as conn:
            result = conn.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            df.to_csv('data/query_result.csv', index=False)

    def execute(self):
        try:
            self.query_results()
            self.logger.warning("Query executed successfully, the result was saved in 'data/query_result.csv'.")
        except Exception as exc:
            self.logger.warning(exc)
            sys.exit(1)


if __name__ == "__main__":
    step = StepTwoQueryOrders()
    step.execute()