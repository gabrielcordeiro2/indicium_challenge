from base_logger import BaseLogger
from datetime import datetime
import pandas as pd
import json
import sys
import os

def data_validated(raw_date):
    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
        return True
    except:
        print("Invalid date, please use 'YYYY-MM-DD'")
        sys.exit(1)


class StepOneOrders(BaseLogger):
    def __init__(self):
        self.logger = self.setup_logger('STEPONE:ORDERS:EXTRACTION')

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

    def csv_to_parquet(self, raw_file_path, separator, date=datetime.now().strftime('%Y-%m-%d')):
        df = pd.read_csv(raw_file_path, sep=separator)
        file_path = f'local_storage/order_details/{date}/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = 'order_details.parquet'
        df.to_parquet(file_path+file_name)

    def execute(self, date=datetime.now().strftime('%Y-%m-%d')):
        try:
            self.csv_to_parquet(raw_file_path="data/order_details.csv", separator=',', date=date)
            self.add_execution_info(data_source='order_details', msg='Success', date=date)
            self.logger.warning("Extraction completed successfully.")
        except Exception as exc:
            self.logger.error(exc, exc_info=True)
            self.add_execution_info(data_source='order_details', msg='Failed', date=date)
            sys.exit(1)


if __name__ == "__main__":
    result = input("Please, type a data to execute the process ex: YYYY-MM-DD ")
    
    if data_validated(result):
        step = StepOneOrders()
        step.execute(date=result) 