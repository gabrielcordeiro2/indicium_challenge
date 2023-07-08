from sqlalchemy import create_engine, text
from sqlalchemy.exc import SAWarning
from base_logger import BaseLogger
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import warnings
import logging
import json
import sys
import os

def data_validated(raw_date):
    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
        return True
    except:
        print("Invalid date, please use 'YYYY-MM-DD'")
        return False

class StepOneNorthwind(BaseLogger):
    def __init__(self):
        warnings.filterwarnings("ignore", category=SAWarning) # Ignore SQLAlchemy Postgres insert Warning
        load_dotenv()
        self.__host = os.getenv("NORTHWIND_HOST")
        self.__user_db = os.getenv("NORTHWIND_USR")
        self.__password_db =  os.getenv("NORTHWIND_PWD")
        self.__database_name = os.getenv("NORTHWIND_DATABASE")
        self.__port = os.getenv("NORTHWIND_PORT")
        self.__engine = create_engine(f'postgresql://{self.__user_db}:{self.__password_db}@{self.__host}:{self.__port}/{self.__database_name}')
        self.logger = self.setup_logger("STEPONE:NORTHWIND:EXTRACTION")

    # def setup_logger(self):
    #     ''' Setup log configuration in 'process_monitor.log' '''
    #     logger = logging.getLogger("STEPONE:NORTHWIND:EXTRACTION")
    #     logger.setLevel(logging.WARNING)
    #     formatter = logging.Formatter("STEPONE:NORTHWIND:EXTRACTION:%(asctime)s:%(message)s", datefmt="%Y:%m:%d_%H:%M")
        
    #     file_handler = logging.FileHandler("process_monitor.log")
    #     file_handler.setFormatter(formatter)
    #     logger.addHandler(file_handler)

    #     stream_handler = logging.StreamHandler()
    #     stream_handler.setFormatter(formatter)
    #     logger.addHandler(stream_handler)
    #     return logger

    def get_tables_list(self, engine, schema):
        query = f""" SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}'; """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            table_names = [row[0] for row in result]
        return table_names

    def read_table_from_database(self, engine, table):
        with engine.connect() as conn:
            df = pd.read_sql_table(table_name=table, con=conn, schema='public')
        return df

    def add_execution_info(self, data_source, msg, date=datetime.now().strftime('%Y-%m-%d')):
        ''' Insert execution status inside 'execution_checker.json' '''
        file_path = 'execution_checker.json'
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                file.write('[{}]')
        with open(file_path, 'r') as file:
            data = json.load(file)

        if not data:
            data = [{}]
        if data[0].get(data_source) is None:
            data[0][data_source] = {}
        if data[0][data_source].get('step1') is None:
            data[0][data_source]['step1'] = {}

        data[0][data_source]['step1'][date] = msg
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)


    def execute(self, date=datetime.now().strftime('%Y-%m-%d')):
        ''' Execute Northwind extraction tasks '''
        try:
            tables = self.get_tables_list(engine=self.__engine, schema='public')
            for table_name in tables:
                df = self.read_table_from_database(engine=self.__engine, table=table_name)
                file_path = f'local_storage/northwind_db/{table_name}/{date}/'
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                file_name = f'{table_name}.parquet'
                df.to_parquet(file_path+file_name)
            self.add_execution_info(data_source='northwind_db', msg='Success', date=date)
            self.logger.warning("Extracao concluida com sucesso.")
        except Exception as exc:
            self.logger.error(exc, exc_info=True)
            self.add_execution_info(data_source='northwind_db', msg='Failed', date=date)
            sys.exit(1)


if __name__ == "__main__":
    result = input("Please, type a data to execute the process ex: YYYY-MM-DD ")
    
    if data_validated(result):
        step = StepOneNorthwind()
        step.execute(date=result)
