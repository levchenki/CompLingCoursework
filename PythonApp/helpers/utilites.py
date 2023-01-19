import re
from itertools import chain
from typing import List, TypeVar

from nltk.corpus import stopwords as nltk_stopwords
from pymorphy3 import MorphAnalyzer

T = TypeVar('T')


# ALL nltk.download RUNS IN DOCKERFILE
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger_ru')
# nltk.download('stopwords')


class UtilsHelper:
    morph = MorphAnalyzer()
    morph_memory = {}
    re_letters = re.compile('[а-я]+')
    re_whitespaces = re.compile(r'\s{2,}')
    stopwords = set(nltk_stopwords.words('russian'))

    @staticmethod
    def chunkify_list(lst: List[T], n: int):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @staticmethod
    def tokenize_lemmatize_stopwords(sentence):
        words = UtilsHelper.re_letters.findall(sentence.lower().replace('ё', 'е'))
        lemmas = map(UtilsHelper.lemmatize_word, words)
        stopped = [word for word in lemmas if word not in UtilsHelper.stopwords]
        return ' '.join(stopped)

    @staticmethod
    def tokenize_line(line: str) -> str:
        return ' '.join(UtilsHelper.re_letters.findall(line.strip().lower().replace('ё', 'е')))

    # @staticmethod
    # def prepare_lines(lines: List[str]) -> List[str]:
    #     rez: List[str] = []
    #     for line in lines:
    #         rez.append(UtilsHelper.tokenize_line(line))
    #     return rez

    @staticmethod
    def lemmatize_word(word: str):
        word = word.strip().lower()
        mem = UtilsHelper.morph_memory.get(word)
        if mem is None:
            mem = UtilsHelper.morph.parse(word)[0].normal_form
            UtilsHelper.morph_memory[word] = mem
        return mem

    @staticmethod
    def lemmatize_many_words(sentence: str):
        return ' '.join([UtilsHelper.lemmatize_word(word) for word in (sentence.split(' '))])

    @staticmethod
    def list_str_split_flatten(arr: List[str]) -> List[str]:
        return list(chain.from_iterable(map(str.split, arr)))

    # @staticmethod
    # def delete_stop_words(sentence: str):
    #     return ' '.join([word for word in sentence.split() if word not in UtilsHelper.stopwords])


UtilsHelper.stopwords.update(['либо', 'это', 'весь', 'еще'])
