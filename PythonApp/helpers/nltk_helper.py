import os
import pickle
import random
from typing import List

import nltk
from nltk import FreqDist, NaiveBayesClassifier

from helpers.directories_helper import DirectoriesHelper
from helpers.logger import Logger
from helpers.utilites import UtilsHelper


class NLTKHelper:
    model: NaiveBayesClassifier
    all_words_freq: set[str]
    __logger = Logger('NLTKHelper')
    __model_path: str
    __words_freq_path: str

    @staticmethod
    async def init(name: str, is_rewrite=False):
        NLTKHelper.__model_path = DirectoriesHelper.temp_dir('models', file_name=f'{name}.pickle')
        NLTKHelper.__words_freq_path = DirectoriesHelper.temp_dir('models', file_name=f'{name}.freq.pickle')
        await NLTKHelper.regenerate_model(is_rewrite=is_rewrite)

    @staticmethod
    def get_tonality(sentence: str) -> str:
        return NLTKHelper.model.classify(dict(
            [word, word in NLTKHelper.all_words_freq]
            for word in UtilsHelper.tokenize_lemmatize_stopwords(sentence).split()
        ))

    @staticmethod
    def __get_tweets_for_model(sentences_list: List[str], frequent_words: set[str]):
        # Создание словаря
        for sentence in sentences_list:
            yield dict([word, word in frequent_words] for word in sentence.split())

    @staticmethod
    async def regenerate_model(is_rewrite=False):
        if is_rewrite and os.path.exists(NLTKHelper.__model_path):
            os.remove(NLTKHelper.__model_path)
        if not os.path.exists(NLTKHelper.__model_path):
            NLTKHelper.__logger.log('[MODEL] generating...')
            NLTKHelper.__logger.start()
            # Считывание CSV
            # n_columns = ['id', 'date', 'name', 'text', 'type', 'rep', 'rtw', 'faw', 'stcount', 'foll', 'frien', 'listcount']
            # pos_csv = pd.read_csv('./RuTweetCorp/positive.csv', sep=';', names=n_columns).drop_duplicates('text', keep='first')['text'].values
            # neg_csv = pd.read_csv('./RuTweetCorp/negative.csv', sep=';', names=n_columns).drop_duplicates('text', keep='first')['text'].values
            # sentences = np.concatenate((pos_csv['text'].values, neg_csv['text'].values))
            # NLTKHelper.__logger.end('read_csv')
            with open('./RuTweetCorp/pos_news.txt', 'r') as f:
                pos_lines = f.readlines()
            with open('./RuTweetCorp/neg_news.txt', 'r') as f:
                neg_lines = f.readlines()
            NLTKHelper.__logger.end('read_txts')
            # Нормализация
            pos_normal_sentences = [UtilsHelper.tokenize_lemmatize_stopwords(text) for text in pos_lines]
            neg_normal_sentences = [UtilsHelper.tokenize_lemmatize_stopwords(text) for text in neg_lines]
            NLTKHelper.__logger.end('normalize')

            # Самые частые слова
            pos_freq_dist = list(FreqDist(UtilsHelper.list_str_split_flatten(pos_normal_sentences)))
            pos_words_freq = set(pos_freq_dist[:int(len(pos_freq_dist) * 0.2)])
            neg_freq_dist = list(FreqDist(UtilsHelper.list_str_split_flatten(neg_normal_sentences)))
            neg_words_freq = set(neg_freq_dist[:int(len(neg_freq_dist) * 0.2)])
            # Сохранение частых слов
            NLTKHelper.all_words_freq = pos_words_freq.union(neg_words_freq)
            with open(NLTKHelper.__words_freq_path, 'wb') as f:
                pickle.dump(NLTKHelper.all_words_freq, f)
            NLTKHelper.__logger.end('FreqDist gen & save')

            # Создание словарей
            positive_tokens_for_model = NLTKHelper.__get_tweets_for_model(pos_normal_sentences, pos_words_freq)
            negative_tokens_for_model = NLTKHelper.__get_tweets_for_model(neg_normal_sentences, neg_words_freq)
            NLTKHelper.__logger.end('Model_dicts')

            # Создание обучающей и тестовой выборки
            positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
            negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]
            NLTKHelper.__logger.end('create_samples')

            # Создание датасета
            dataset = positive_dataset + negative_dataset
            random.shuffle(dataset)
            knife = int(len(dataset) * 0.95)
            train_data = dataset[:knife]
            test_data = dataset[knife:]
            NLTKHelper.__logger.end('create_dataset')

            # Обучение
            NLTKHelper.model = NaiveBayesClassifier.train(train_data)
            NLTKHelper.__logger.end('training')
            print("Accuracy is:", nltk.classify.accuracy(NLTKHelper.model, test_data))
            print(NLTKHelper.model.show_most_informative_features(10))

            # Сохранение модели
            NLTKHelper.__logger.start()
            with open(NLTKHelper.__model_path, 'wb') as f:
                pickle.dump(NLTKHelper.model, f)
            NLTKHelper.__logger.end('save model')
            NLTKHelper.__logger.log('[MODEL] generated and loaded!')
        else:
            NLTKHelper.__logger.log(f'[MODEL] loading... {NLTKHelper.__model_path};\t{NLTKHelper.__words_freq_path}')
            with open(NLTKHelper.__model_path, 'rb') as f:
                NLTKHelper.model = pickle.load(f)
            with open(NLTKHelper.__words_freq_path, 'rb') as f:
                NLTKHelper.all_words_freq = pickle.load(f)
            NLTKHelper.__logger.log(f'[MODEL] loaded! FreqDist: {len(NLTKHelper.all_words_freq)}')
