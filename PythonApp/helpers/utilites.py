import re
from typing import List

from pymorphy2 import MorphAnalyzer


class UtilsHelper:
    morph = MorphAnalyzer()
    morph_memory = {}

    @staticmethod
    def tokenize_line(line: str) -> str:
        return ' '.join(re.findall('[а-яё]+', line.strip().lower()))

    @staticmethod
    def prepare_lines(lines: List[str]) -> List[str]:
        rez: List[str] = []
        for line in lines:
            rez.append(UtilsHelper.tokenize_line(line))
        return rez

    @staticmethod
    def lemmatize_word(word: str):
        word = word.strip().lower()
        mem = UtilsHelper.morph_memory.get(word)
        if mem is not None:
            return mem
        else:
            mem = UtilsHelper.morph.parse(word)[0].normal_form
            UtilsHelper.morph_memory[word] = mem
        return mem

    @staticmethod
    def lemmatize_many_words(sentence: str):
        return ' '.join([UtilsHelper.lemmatize_word(word) for word in (sentence.split(' '))])
