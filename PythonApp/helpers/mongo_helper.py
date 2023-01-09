import os
import shutil

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from helpers.directories_helper import DirectoriesHelper
from helpers.logger import Logger
from helpers.utilites import UtilsHelper


class MongoHelper:
    __logger = Logger('MongoHelper').log

    client: MongoClient
    db: Database
    news_collection: Collection
    people_collection: Collection

    def __init__(self):
        user = os.environ["MONGODB_USER"]
        password = os.environ["MONGODB_PASS"]
        host = os.environ["MONGODB_HOST"]
        port = os.environ["MONGODB_PORT"]
        MongoHelper.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
        MongoHelper.db = MongoHelper.client.get_database('bloknot-parser')
        MongoHelper.news_collection = MongoHelper.db.get_collection('news')
        MongoHelper.people_collection = MongoHelper.db.get_collection('people')

    @staticmethod
    def generate_news_txt_files(news_txt_files_dir: str, is_rewrite: bool = False):
        new_news_count = MongoHelper.tokenize_lemmatize_news()
        news_list = list(MongoHelper.news_collection.find())
        if new_news_count == 0 and not is_rewrite and len(os.listdir(news_txt_files_dir)) == len(news_list):
            return
        if os.path.exists(news_txt_files_dir):
            shutil.rmtree(news_txt_files_dir, ignore_errors=True)
        DirectoriesHelper.ensure_dir(news_txt_files_dir)
        MongoHelper.__logger('[GENERATING] news txt files...')
        for news_item in news_list:
            with open(
                    file=os.path.join(news_txt_files_dir, f'news_item_{news_item.get("_id")}.txt'),
                    mode='w',
                    encoding='utf-8'
            ) as file:
                file.write(news_item.get('prepared'))
        MongoHelper.__logger('[COMPLETE] news txt files')

    @staticmethod
    def tokenize_lemmatize_news():
        news = list(MongoHelper.news_collection.find({'prepared': None}))
        news_count = len(news)
        for i, news_item in enumerate(news):
            # title_content = f'{news_item.get("title")} {news_item.get("text")}'
            content = news_item.get("text")
            tokenized_line = UtilsHelper.tokenize_line(content)
            lemmatized_line = UtilsHelper.lemmatize_many_words(tokenized_line)
            MongoHelper.news_collection.update_one(
                {'_id': news_item['_id']},
                {'$set': {'prepared': lemmatized_line}},
            )
            if i % 250 == 0:
                MongoHelper.__logger(f'tokenize_lemmatize: {round(i / news_count * 100)}% {i} / {news_count}')
        MongoHelper.__logger('[COMPLETE] tokenize_lemmatize')
        return news_count
