from sqlalchemy import create_engine, text
from base_logger import BaseLogger
from dotenv import load_dotenv
import logging
import sys
import os

class StepTwoCreateTables(BaseLogger):
    def __init__(self):
        load_dotenv()
        self.__host = os.getenv("DBFINAL_HOST")
        self.__user_db = os.getenv("DBFINAL_USR")
        self.__password_db =  os.getenv("DBFINAL_PWD")
        self.__database_name = os.getenv("DBFINAL_DATABASE")
        self.__port = os.getenv("DBFINAL_PORT")
        self.__engine = create_engine(f'postgresql://{self.__user_db}:{self.__password_db}@{self.__host}:{self.__port}/{self.__database_name}')
        self.logger = self.setup_logger("STEPTWO:CREATETABLES")

    # def setup_logger(self):
    #     ''' Setup log configuration in 'process_monitor.log' '''
    #     logger = logging.getLogger("STEPTWO:CREATETABLES")
    #     logger.setLevel(logging.WARNING)
    #     formatter = logging.Formatter("STEPTWO:CREATETABLES:%(asctime)s:%(message)s", datefmt="%Y:%m:%d_%H:%M")
        
    #     file_handler = logging.FileHandler("process_monitor.log")
    #     file_handler.setFormatter(formatter)
    #     logger.addHandler(file_handler)

    #     stream_handler = logging.StreamHandler()
    #     stream_handler.setFormatter(formatter)
    #     logger.addHandler(stream_handler)
    #     return logger
    
    def create_database_tables(self):
        with self.__engine.connect() as connection:
            with open('data/final_db_table_definitions.sql') as f:
                data = f.read()
                connection.execute(text(data))
                connection.commit()
    
    def execute(self):
        try:
            self.create_database_tables()
            self.logger.warning("Tables created successfully.")
        except Exception as exc:
            self.logger.error(exc, exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    
    step = StepTwoCreateTables()
    step.execute()


