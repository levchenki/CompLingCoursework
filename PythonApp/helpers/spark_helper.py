import json
import os
import shutil
import string

from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import Word2Vec
from pyspark.ml.feature import Word2VecModel
from pyspark.sql import SparkSession

from helpers.directories_helper import DirectoriesHelper
from helpers.logger import Logger


class SparkHelper:
    model: Word2VecModel
    __logger = Logger('SparkHelper').log

    def __init__(self, name: str, txt_file_path: str, is_rewrite: bool = False):
        self.__name = name
        self.__txt_files_dir = txt_file_path
        self.__model_path = DirectoriesHelper.temp_dir('models', file_name=name)
        # init pyspark
        self.sparkClient = SparkSession \
            .builder \
            .appName("Word2VecApplication") \
            .getOrCreate()
        # generate model
        self.regenerate_news_model(is_rewrite=is_rewrite)

    def regenerate_news_model(self, is_rewrite: bool = False):
        if is_rewrite and os.path.exists(self.__model_path):
            shutil.rmtree(self.__model_path, ignore_errors=True)
        if not os.path.exists(self.__model_path):
            self.__logger('[MODEL] generating... ~15min')
            # Построчная загрузка файла
            assert os.path.exists(self.__txt_files_dir), f'{self.__txt_files_dir} not exists!'
            # input_file = self.sparkClient.sparkContext.textFile(self.__txt_files_dir)
            # prepared = input_file.map(lambda x: ([x]))
            # data_frame = prepared.toDF()
            # prepared_data_frame = data_frame.selectExpr('_1 as text')
            prepared_input_data = self.sparkClient.sparkContext.wholeTextFiles(self.__txt_files_dir) \
                .map(lambda x: (x[0], x[1].translate(str.maketrans('', '', string.punctuation))))
            prepared_data_frame = prepared_input_data.toDF().selectExpr('_1 as path', '_2 as text')
            # Разбить на токены
            words = Tokenizer(inputCol='text', outputCol='words').transform(prepared_data_frame)
            # Удалить стоп-слова
            stop_words = StopWordsRemover.loadDefaultStopWords('russian')
            remover = StopWordsRemover(inputCol='words', outputCol='filtered', stopWords=stop_words)
            filtered = remover.transform(words)
            # Вывести таблицу filtered
            # filtered.show()
            # Вывести столбец таблицы words с токенами до удаления стоп-слов
            # words.select('words').show(truncate=False, vertical=True)
            # Вывести столбец "filtered" таблицы filtered с токенами после удаления стоп-слов
            # filtered.select('filtered').show(truncate=False, vertical=True)
            # word2vec = Word2Vec(vectorSize=3, inputCol='filtered', outputCol='result')
            word2vec = Word2Vec(inputCol='filtered', outputCol='result')
            model = word2vec.fit(filtered)
            w2v_df = model.transform(filtered)
            w2v_df.show()
            model.save(self.__model_path)
            self.__logger('[MODEL] generated!')
        self.__logger('[MODEL] loading... ~5sec')
        self.model: Word2VecModel = Word2VecModel.load(self.__model_path)
        self.__logger('[MODEL] loaded!')

    def get_synonyms(self, entry_word: str):
        self.__logger(f'search synonyms for {entry_word}...')
        try:
            entry_word = entry_word.replace(' ', '').lower()
            synonyms = self.model.findSynonyms(entry_word, 30)  # .show()
            return [json.loads(el) for el in synonyms.toJSON().collect()]
        except Exception as ex:
            print("Данного слова нет в словаре!")
            print(ex)
            return {'error': 'Данного слова нет в словаре!'}
