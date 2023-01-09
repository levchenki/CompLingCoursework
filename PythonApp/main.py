from helpers.directories_helper import DirectoriesHelper
from helpers.mongo_helper import MongoHelper
from helpers.spark_helper import SparkHelper
from flask import Flask, request  # , jsonify

app = Flask('python-word2vec-app')


@app.route('/synonyms', methods=['GET'])
def get_synonyms():
    word = request.args.get('w')
    if word is None or len(word) == 0:
        return 'Необходимо передать слово в параметр w', 401
    return spark_helper.get_synonyms(word)


if __name__ == '__main__':
    mongo_helper = MongoHelper()
    mongo_helper.generate_news_txt_files(news_txt_files_dir=DirectoriesHelper.news_txt_files_dir())
    spark_helper = SparkHelper(name='news', txt_file_path=DirectoriesHelper.news_txt_files_dir())
    app.run(debug=True, host='0.0.0.0', port=5000)

# mongo_helper = MongoHelper()
# mongo_helper.generate_news_txt_files(news_txt_files_dir=DirectoriesHelper.news_txt_files_dir())
# spark_helper = SparkHelper(name='news', txt_file_path=DirectoriesHelper.news_txt_files_dir())
# park_helper.get_synonyms('волгоград')
# spark_helper.get_synonyms('бочаров')
# spark_helper.get_synonyms('парк')
# spark_helper.get_synonyms('волга')
