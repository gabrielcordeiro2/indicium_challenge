from sqlalchemy import create_engine, text
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import logging
import sys
import os


class StepTwoQueryOrders:
    def __init__(self):
        load_dotenv()
        self.__host = os.getenv("DBFINAL_HOST")
        self.__user_db = os.getenv("DBFINAL_USR")
        self.__password_db =  os.getenv("DBFINAL_PWD")
        self.__database_name = os.getenv("DBFINAL_DATABASE")
        self.__port = os.getenv("DBFINAL_PORT")
        self.__engine = create_engine(f'postgresql://{self.__user_db}:{self.__password_db}@{self.__host}:{self.__port}/{self.__database_name}')
        self.logger = self.setup_logger()
        self.order_details_path = 'local_storage/order_details/'

    def setup_logger(self):
        ''' Setup log configuration in 'process_monitor.log' '''
        logger = logging.getLogger("STEPTWO:QUERYRESULTS")
        logger.setLevel(logging.WARNING)
        if not logger.handlers:
            formatter = logging.Formatter("STEPTWO:QUERYRESULTS:%(asctime)s:%(message)s", datefmt="%Y:%m:%d_%H:%M")
            file_handler = logging.FileHandler("process_monitor.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
        return logger
    
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
            self.logger.warning("Query executada com sucesso, o resultado foi salvo em 'data/query_result.csv'.")
        except Exception as exc:
            self.logger.warning(exc)
            sys.exit(1)


if __name__ == "__main__":
    step = StepTwoQueryOrders()
    step.execute()