IS_LOGGING = True


class Logger:
    name: str

    def __init__(self, name: str):
        self.name = name

    def log(self, log_str: str):
        if not IS_LOGGING:
            return
        print(f'[{self.name}] {log_str}')
