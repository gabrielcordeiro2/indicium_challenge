import logging

class BaseLogger:
    ''' Logger Template for use logs '''
    def setup_logger(self, logger_name='MAIN:EXECUTOR'):
        ''' Setup log configuration in 'process_monitor.log' '''
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)
        formatter = logging.Formatter(f"{logger_name}:%(asctime)s:%(message)s", datefmt="%Y:%m:%d_%H:%M")
        
        file_handler = logging.FileHandler("process_monitor.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger