import os


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
