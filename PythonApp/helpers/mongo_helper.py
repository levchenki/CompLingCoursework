import asyncio
import math
import os
import re
import shutil
from datetime import datetime
from typing import Optional
from xml.etree import ElementTree

from beanie import Document, Link, init_beanie, Indexed
from beanie.odm.operators.find.logical import Nor
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient

from helpers.directories_helper import DirectoriesHelper
from helpers.logger import Logger
from helpers.nltk_helper import NLTKHelper
from helpers.utilites import UtilsHelper


class NewsItem(Document):
    class Settings:
        name = 'news'

    title: str
    text: str
    link: str

    prepared: Optional[str]
    places: Optional[str]
    persons: Optional[str]

    _class: str
    commentsCount: int
    date: datetime


class NewsSentences(Document):
    class Settings:
        name = 'sentences'

    title: str
    link: str
    news_ref: Link[NewsItem]

    detected: Indexed(str)
    sentence: Indexed(str)
    type: str
    tonality: str


class MongoHelper:
    __logger = Logger('MongoHelper')

    @staticmethod
    async def init():
        user = os.environ["MONGODB_USER"]
        password = os.environ["MONGODB_PASS"]
        host = os.environ["MONGODB_HOST"]
        port = os.environ["MONGODB_PORT"]
        client = AsyncIOMotorClient(f'mongodb://{user}:{password}@{host}:{port}')
        await init_beanie(
            database=client['bloknot-parser'],
            document_models=[NewsItem, NewsSentences]
        )

    @staticmethod
    async def perform_tomita_and_tonality():
        news = await NewsItem.find({NewsItem.places: None, NewsItem.persons: None}).to_list()
        # будем порционно обрабатывать новости Томитой
        news_chunks = UtilsHelper.chunkify_list(news, 2000)
        news_chunks_count = math.ceil(len(news) / 2000)
        re_white_spaces = re.compile(r'\s{2,}')
        # news_chunks это массив массивов новостей, теперь нужно каждый чанк обработать томитой
        if news_chunks_count > 0:
            MongoHelper.__logger.log(f'[TOMITA & TONALITY] start generating: {len(news)} news')
        for chunk_index, chunk in enumerate(news_chunks):
            # создаем input.txt, где каждая новая строчка - отдельный документ
            input_file_lines = [re_white_spaces.sub(' ', news_item.text).strip() + '\n' for news_item in chunk]
            unprocessed_docs = set(range(len(chunk)))
            with open(DirectoriesHelper.tomita_input, 'w') as file:
                file.writelines(input_file_lines)
            # запускаем Томиту
            await (await asyncio.create_subprocess_exec(
                *DirectoriesHelper.tomita_command().split(' '),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )).communicate()
            # обрабатываем результат Томиты
            xml_root = ElementTree.parse(DirectoriesHelper.tomita_output).getroot()
            for document in xml_root:
                doc_index = int(document.attrib['di']) - 1
                unprocessed_docs.remove(doc_index)
                doc_persons: set[str] = set()
                doc_places: set[str] = set()
                # Вытаскиваем из документа факты и предложения
                for fact, lead in zip(document.find('facts'), document.find('Leads')):
                    soup = BeautifulSoup(lead.attrib.get('text'), 'lxml')
                    type_ = fact.tag
                    p_element = soup.find('p')
                    if p_element is None:
                        continue
                    lemma = p_element.attrs.get('lemma')
                    sentence = soup.text[21:]
                    # Если запись с такой же сущностью в таком же предложении уже существует, то игнорируем текущую
                    if await NewsSentences.find_one({NewsSentences.detected: lemma, NewsSentences.sentence: sentence}) is not None:
                        continue
                    tonality = NLTKHelper.get_tonality(sentence)
                    # Создаём новую запись с предложением и что в нём нашлось
                    await NewsSentences(
                        news_ref=chunk[doc_index],
                        title=chunk[doc_index].title,
                        link=chunk[doc_index].link,
                        sentence=sentence,
                        detected=lemma,
                        tonality=tonality,
                        type=type_,
                    ).insert()
                    doc_persons.add(lemma) if type_ == 'Person' else doc_places.add(lemma)
                # Записываем в новость все объекты, что в ней нашлись
                chunk[doc_index].persons = ', '.join(doc_persons)
                chunk[doc_index].places = ', '.join(doc_places)
                await chunk[doc_index].save()
            # В новости, в которых ничего не нашлось, впишем заглушки для последующих запусков приложения
            for unprocessed_doc_index in unprocessed_docs:
                chunk[unprocessed_doc_index].persons = ''
                chunk[unprocessed_doc_index].places = ''
                await chunk[unprocessed_doc_index].save()
            # Логирование
            chunk_num = chunk_index + 1
            MongoHelper.__logger.log(f'[TOMITA & TONALITY] processed: {round(chunk_num / news_chunks_count * 100)}% {chunk_num} / {news_chunks_count}')
        MongoHelper.__logger.log('[TOMITA & TONALITY] complete')

    @staticmethod
    async def generate_news_txt_files(news_txt_files_dir: str, is_rewrite: bool = False):
        new_news_count = await MongoHelper.tokenize_lemmatize_news()
        news_list = await NewsItem.find(Nor({NewsItem.prepared: None})).to_list()
        if new_news_count == 0 and not is_rewrite and len(os.listdir(news_txt_files_dir)) == len(news_list):
            return
        if os.path.exists(news_txt_files_dir):
            shutil.rmtree(news_txt_files_dir, ignore_errors=True)
        DirectoriesHelper.ensure_dir(news_txt_files_dir)
        MongoHelper.__logger.log('[NEWS_TXT_FILES] generating...')
        for news_item in news_list:
            with open(
                    file=os.path.join(news_txt_files_dir, f'news_item_{news_item.id}.txt'),
                    mode='w',
                    encoding='utf-8'
            ) as file:
                file.write(news_item.prepared)
        MongoHelper.__logger.log('[NEWS_TXT_FILES] complete')

    @staticmethod
    async def tokenize_lemmatize_news():
        news = await NewsItem.find({NewsItem.prepared: None}).to_list()
        news_count = len(news)
        if news_count > 0:
            MongoHelper.__logger.log(f'[TOKENIZE_LEMMATIZE] start processing {news_count} news...')
        for i, news_item in enumerate(news):
            tokenized_line = UtilsHelper.tokenize_line(news_item.text)
            lemmatized_line = UtilsHelper.lemmatize_many_words(tokenized_line)
            news_item.prepared = lemmatized_line
            await news_item.save()
            if i % 250 == 0:
                MongoHelper.__logger.log(f'[TOKENIZE_LEMMATIZE] {round(i / news_count * 100)}% {i} / {news_count}')
        MongoHelper.__logger.log('[TOKENIZE_LEMMATIZE] complete')
        return news_count
