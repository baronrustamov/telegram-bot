import os, io
import errno
import urllib
import urllib.request
import hashlib
import re
import requests
from time import sleep
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from urllib.request import urlopen, Request
'''
from bs4 import BeautifulSoup
import pandas as pd
from ast import literal_eval
from cdqa.utils.filters import filter_paragraphs
from cdqa.utils.download import download_model, download_bnpp_data
from cdqa.pipeline.cdqa_sklearn import QAPipeline
from cdqa.utils.converters import pdf_converter
'''
result_urls = []

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'idkey.json'

client = vision_v1.ImageAnnotatorClient()

FILE_NAME = '1.jpg'

with io.open(os.path.join(FILE_NAME), 'rb') as image_file:
    content = image_file.read()

#image = vision_v1.types.Image(content=content)
image = vision_v1.Image(content=content)
response = client.web_detection(image=image)
ant = response.web_detection
#texts = response.text_annotations[0]
# print(texts.description)

texts = response.text_annotations
'''
if '?' in texts.description:
    question = re.search('([^?]+)', texts.description).group(1)

elif ':' in texts.description:
    question = re.search('([^:]+)', texts.description).group(1)

elif '\n' in texts.description:
    question = re.search('([^\n]+)', texts.description).group(1)

slugify_keyword = urllib.parse.quote_plus(question)
# print(slugify_keyword)

def crawl_result_urls():
    req = Request('https://google.com/search?q=' + slugify_keyword, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    results = bs.find_all('div', class_='ZINbbc')
    try:
        for result in results:
            link = result.find('a')['href']
            print(link)
            if 'url' in link:
                result_urls.append(re.search('q=(.*)&sa', link).group(1))
    except (AttributeError, IndexError) as e:
        pass

def get_result_details(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        bs = BeautifulSoup(html, 'html.parser')
        try:
            title =  bs.find(re.compile('^h[1-6]$')).get_text().strip().replace('?', '').lower()
            # Set your path to pdf directory
            filename = "/path/to/pdf_folder/" + title + ".pdf"
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            with open(filename, 'w') as f:
                for line in bs.find_all('p')[:5]:
                    f.write(line.text + '\n')
        except AttributeError:
            pass
    except urllib.error.HTTPError:
        pass

def find_answer():
    # Set your path to pdf directory
    df = pdf_converter(directory_path='/path/to/pdf_folder/')
    cdqa_pipeline = QAPipeline(reader='models/bert_qa.joblib')
    cdqa_pipeline.fit_retriever(df)
    query = question + '?'
    prediction = cdqa_pipeline.predict(query)

    # print('query: {}\n'.format(query))
    # print('answer: {}\n'.format(prediction[0]))
    # print('title: {}\n'.format(prediction[1]))
    # print('paragraph: {}\n'.format(prediction[2]))
    return prediction[0]

crawl_result_urls()

for url in result_urls[:3]:
    get_result_details(url)
    sleep(5)

answer = find_answer()
print('Answer: ' + answer)
'''
print(ant)