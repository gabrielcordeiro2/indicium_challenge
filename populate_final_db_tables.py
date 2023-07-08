from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from base_logger import BaseLogger
from dotenv import load_dotenv
import pandas as pd
import logging
import json
import sys
import os


def check_execution_status(date, logger=logging):
    ''' Checks whether all processes in StepOne of a specific date were successfully executed. '''
    try:
        file_path = 'execution_checker.json'
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                file.write('[{}]')

        with open('execution_checker.json', 'r') as file:
            data = json.load(file)

        if data[0].get('northwind_db') is None:
            data[0]['northwind_db'] = {}
            data[0]['northwind_db']['step1'] = {}
        if data[0].get('order_details') is None:
            data[0]['order_details'] = {}
            data[0]['order_details']['step1'] = {}
        

        northwind_status = data[0]['northwind_db']['step1'].get(date)
        orders_status = data[0]['order_details']['step1'].get(date)

        if northwind_status == "Failed" or orders_status == "Failed":
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            new_date = date_obj+timedelta(days=1)
            new_date = new_date.strftime("%Y-%m-%d")
            logger.warning(f"Erro no processo de carregamento em '{date}', execute a etapa 1 de extracao do novamente no dia '{new_date}'.")
            sys.exit(1)

        # if not northwind_status:
        #     logger.warning("Por favor, execute o processo de 'Northwind_db' de extracao da data especificada.")
        #     sys.exit(1)
        # if not orders_status:
        #     logger.warning("Por favor, execute o processo de 'Order_details' de extracao da data especificada.")
        #     sys.exit(1)

    except Exception as exc:
        logging.error(exc, exc_info=True)
        sys.exit(1)

def data_validated(raw_date):
    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
        return True
    except:
        print("Invalid date, please use 'YYYY-MM-DD'")
        return False

class NorthwindToFinalDB(BaseLogger):
    def __init__(self):
        load_dotenv()
        self.__host = os.getenv("DBFINAL_HOST")
        self.__user_db = os.getenv("DBFINAL_USR")
        self.__password_db =  os.getenv("DBFINAL_PWD")
        self.__database_name = os.getenv("DBFINAL_DATABASE")
        self.__port = os.getenv("DBFINAL_PORT")
        self.__engine = create_engine(f'postgresql://{self.__user_db}:{self.__password_db}@{self.__host}:{self.__port}/{self.__database_name}')
        self.__logger = self.setup_logger("STEPTWO:NORTHWIND:LOAD")
        self._northwind_path = 'local_storage/northwind_db/'
    
    def setup_initial_paths(self):
        if not os.path.exists(self._northwind_path):
            os.makedirs(self._northwind_path)
        northwind_tables = os.listdir(self._northwind_path)
        if not northwind_tables:
            self.__logger.warning("Tabelas de 'Northwind' nao foram carregadas.")
            sys.exit(1)
        return northwind_tables

    def populate_database(self, date, tables):
        for table in tables:
            file_path = f'local_storage/northwind_db/{table}/{date}/{table}.parquet'
            df = pd.read_parquet(file_path)
            with self.__engine.begin() as conn:
                df.to_sql(name=table ,schema='public',con=conn, if_exists='append', index=False)

    def execute(self, date=datetime.now().strftime('%Y-%m-%d')):
        try:
            tables = self.setup_initial_paths()

            self.populate_database(date, tables)
            self.__logger.warning("Carregamento concluido com sucesso.")
        except Exception as exc:
            self.__logger.error(exc, exc_info=True)
            sys.exit(1)


class OrdersToFinalDB(BaseLogger):
    def __init__(self):
        load_dotenv()
        self.__host = os.getenv("DBFINAL_HOST")
        self.__user_db = os.getenv("DBFINAL_USR")
        self.__password_db =  os.getenv("DBFINAL_PWD")
        self.__database_name = os.getenv("DBFINAL_DATABASE")
        self.__port = os.getenv("DBFINAL_PORT")
        self.__engine = create_engine(f'postgresql://{self.__user_db}:{self.__password_db}@{self.__host}:{self.__port}/{self.__database_name}')
        self.logger = self.setup_logger("STEPTWO:ORDERS:LOAD")
        self.order_details_path = 'local_storage/order_details/'
    
    def setup_initial_paths(self):
        if not os.path.exists(self.order_details_path):
            os.makedirs(self.order_details_path)
        order_details_table = os.listdir(self.order_details_path)
        if not order_details_table:
            self.logger.warning("Tabela de 'Order_details' nao foi carregada.")
            sys.exit(1)

    def populate_database(self, date):
        file_path = f'local_storage/order_details/{date}/order_details.parquet'
        df = pd.read_parquet(file_path)
        base_path = os.path.basename(file_path)
        table_name = os.path.splitext(base_path)[0]
        with self.__engine.begin() as conn:
            df.to_sql(name=table_name ,schema='public',con=conn, if_exists='append', index=False)

    def execute(self, date=datetime.now().strftime('%Y-%m-%d')):
        try:
            self.setup_initial_paths()
            self.populate_database(date=date)
            self.logger.warning("Carregamento concluido com sucesso.")
        except Exception as exc:
            self.logger.error(exc, exc_info=True)



if __name__ == "__main__":
    result = input("Please, type a data to execute the process ex: YYYY-MM-DD ")
    if data_validated(result):
        check_execution_status(date=result, logger=BaseLogger().setup_logger('STEPTWO:POPULATE:CHECKER'))
        step_northwind = NorthwindToFinalDB()
        step_orders = OrdersToFinalDB()
        step_northwind.execute(date=result)
        step_orders.execute(date=result)

