import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from helpers.directories_helper import DirectoriesHelper
from helpers.mongo_helper import MongoHelper, NewsSentences
from helpers.nltk_helper import NLTKHelper
from helpers.spark_helper import SparkHelper

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=['http://0.0.0.0:5000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def on_startup():
    global spark_helper
    await asyncio.gather(
        MongoHelper.init(),
        NLTKHelper.init(name='tonality_classifier_test1')
    )
    await asyncio.gather(
        MongoHelper.generate_news_txt_files(news_txt_files_dir=DirectoriesHelper.news_txt_files_dir()),
        MongoHelper.perform_tomita_and_tonality(),
    )
    spark_helper = SparkHelper(name='news', txt_file_path=DirectoriesHelper.news_txt_files_dir())


@app.get('/synonyms')
def get_synonyms(word: str):
    if word is None or len(word) == 0:
        return 'Необходимо передать слово в параметр w', 401
    return spark_helper.get_synonyms(word)


@app.get('/marked-sentences')
async def get_tomita(page: int = 1, count: int = 20):
    offset = (page - 1) * count
    return {
        'total': await NewsSentences.find().count(),
        'sentences': (await NewsSentences.find().to_list())[offset:offset + count],
    }


@app.get('/tonality')
async def get_tonality(sentence: str):
    return NLTKHelper.get_tonality(sentence)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
