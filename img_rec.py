import os, io
import errno
import urllib
import urllib.request
import hashlib
import re
import requests
from time import sleep
import json
#from protobuf_to_dict import protobuf_to_dict
from google.protobuf.json_format import MessageToJson, MessageToDict, Parse
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from urllib.request import urlopen, Request
#from run import image_name

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

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vidkey.json'

client = vision_v1.ImageAnnotatorClient()
#FILE_NAME = 'file_0.jpg'



def recog(image_name):
    with io.open(os.path.join(image_name), 'rb') as image_file:
        content = image_file.read()
    #image = vision_v1.types.Image(content=content)
    image = vision_v1.Image(content=content)
    response = client.web_detection(image=image)
    annotations = response.web_detection
    res = annotations.__class__.to_json(annotations)
    dataimg = json.loads(res)
    jdump = json.dumps(res,indent=4)
    print(dataimg["webEntities"][0]["description"])
    print(dataimg)
    print(res)
    print(jdump)
    out = dataimg["webEntities"][0]["description"] + '\n' + '\n'
    #out = out + dataimg["webEntities"][1]["description"] + '\n' + '\n'
    #out = out + dataimg["webEntities"][2]["description"] + '\n' + '\n'
    #return out


txt = '''
hi
aloha
zdraste
'''
print(txt)



'''
if annotations.best_guess_labels:
    for label in annotations.best_guess_labels:
        print('\nBest guess label: {}'.format(label.label))

if annotations.pages_with_matching_images:
    print('\n{} Pages with matching images found:'.format(
        len(annotations.pages_with_matching_images)))

    for page in annotations.pages_with_matching_images:
        print('\n\tPage url   : {}'.format(page.url))

            if page.full_matching_images:
                print('\t{} Full Matches found: '.format(
                       len(page.full_matching_images)))

                for image in page.full_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

            if page.partial_matching_images:
                print('\t{} Partial Matches found: '.format(
                       len(page.partial_matching_images)))

                for image in page.partial_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))

    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

        for image in annotations.visually_similar_images:
            print('\tImage url    : {}'.format(image.url))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # [END vision_python_migration_web_detection]
# [END vision_web_detection]

'''

#texts = response.text_annotations[0]
# print(texts.description)
#texts = response.text_annotations
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
