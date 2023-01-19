import os
import platform


class DirectoriesHelper:
    @staticmethod
    def temp_dir(*path: str, file_name: str = None) -> str:
        dir_path = os.path.join('', 'temp', *path)
        os.makedirs(dir_path, exist_ok=True)
        if file_name:
            dir_path = os.path.join(dir_path, file_name)
        return os.path.abspath(dir_path)

    @staticmethod
    def news_txt_files_dir() -> str:
        return DirectoriesHelper.temp_dir('news_txt_files')

    @staticmethod
    def ensure_dir(path: str):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    tomita_input = os.path.abspath('./tomita_runnable/input.txt')
    tomita_output = os.path.abspath('./tomita_runnable/output.xml')

    @staticmethod
    def tomita_command() -> str:
        tomita_ext = '.exe' if platform.system() == 'Windows' else ''
        tomita_binary = os.path.abspath(f'./tomita_runnable/tomita-parser{tomita_ext}')
        config_proto = os.path.abspath('./tomita_runnable/config.proto')
        assert os.path.exists(tomita_binary), 'tomita binary not found'
        assert os.path.exists(config_proto), 'tomita config_proto not found'
        return f'{tomita_binary} {config_proto}'
