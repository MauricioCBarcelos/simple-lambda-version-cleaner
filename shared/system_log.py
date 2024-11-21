import datetime
import logging
import os


class SystemLogger(logging.Logger):
    def __init__(self, name, log_output_path, log_file_name, level=logging.INFO):
        super().__init__(name, level)
        if not os.path.exists(log_output_path):
            os.makedirs(log_output_path)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename = f"{log_output_path}/{log_file_name}_{timestamp}.log"
        log_format = (
            "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s"
        )

        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        self.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_formatter)
        self.addHandler(console_handler)
