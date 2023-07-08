from northwind_to_parquet import StepOneNorthwind
from orders_to_parquet import StepOneOrders
from create_final_db_tables import StepTwoCreateTables
from populate_final_db_tables import NorthwindToFinalDB, OrdersToFinalDB, check_execution_status
from query_orders import StepTwoQueryOrders
from base_logger import BaseLogger

from datetime import datetime
import logging

def data_validated(raw_date):
    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
        return True
    except:
        print("Invalid date, please use 'YYYY-MM-DD'")
        return False

class IndiciumPipeline(BaseLogger):
    def __init__(self):
        self.logger = self.setup_logger("MAIN:EXECUTOR")

    # def setup_logger(self):
    #     ''' Setup log configuration in 'process_monitor.log' '''
    #     logger = logging.getLogger("MAIN:EXECUTOR")
    #     logger.setLevel(logging.WARNING)
    #     if not logger.handlers:
    #         formatter = logging.Formatter("MAIN:EXECUTOR:%(asctime)s:%(message)s", datefmt="%Y:%m:%d_%H:%M")

    #         file_handler = logging.FileHandler("process_monitor.log")
    #         file_handler.setFormatter(formatter)
    #         logger.addHandler(file_handler)

    #         stream_handler = logging.StreamHandler()
    #         stream_handler.setFormatter(formatter)
    #         logger.addHandler(stream_handler)
    #     return logger
    
    def execute(self, date):
        self.logger.warning("Starting pipeline ...")
        self.logger.warning("Starting Step One ...")

        step_one_northwind_extraction = StepOneNorthwind()
        step_one_orders_extraction = StepOneOrders()

        check_execution_status(date=date, logger=self.logger)
        step_one_northwind_extraction.execute(date)
        step_one_orders_extraction.execute(date)

        self.logger.warning("Step One executed successfully.")
        self.logger.warning("Starting Step Two ...")

        step_two_create_tables = StepTwoCreateTables()
        step_two_northwind_populate_finaldb = NorthwindToFinalDB()
        step_two_orders_populate_finaldb = OrdersToFinalDB()
        step_two_query_orders = StepTwoQueryOrders()

        step_two_create_tables.execute()
        step_two_northwind_populate_finaldb.execute(date)
        step_two_orders_populate_finaldb.execute(date)
        step_two_query_orders.execute()
        
        self.logger.warning("Step Two executed successfully.")
        self.logger.warning("Pipeline finished.")



if __name__ == "__main__":
    result = input("Please, type a data to execute the process ex: YYYY-MM-DD ")
    
    if data_validated(result):
        pipeline = IndiciumPipeline()
        pipeline.execute(result)

