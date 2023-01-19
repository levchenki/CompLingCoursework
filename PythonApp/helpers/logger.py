import time
from datetime import timedelta

IS_LOGGING = True


def create_logger(name: str):
    return lambda log_str: print(f'[{name}] {log_str}')


class Logger:
    name: str
    __total = time.monotonic()
    __start_time = time.monotonic()

    def __init__(self, name: str):
        self.name = name

    def log(self, log_str: str):
        if not IS_LOGGING:
            return
        print(f'[{self.name}] {log_str}')

    def start(self):
        self.__start_time = time.monotonic()

    def end(self, complete_event_name: str = None):
        print(f'[{self.name}]', end='\t')
        if complete_event_name is not None:
            print(f'[{complete_event_name.upper()}]', end='\t')
        print(
            'total', timedelta(seconds=time.monotonic() - Logger.__total),
            'measurement', timedelta(seconds=time.monotonic() - self.__start_time),
            sep='\t'
        )
        self.start()
