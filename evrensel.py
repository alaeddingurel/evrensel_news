#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 15:00:23 2019

@author: user
"""

from bs4 import BeautifulSoup

import codecs
from lxml import etree
import glob
import pandas as pd


file = codecs.open("https___www.evrensel.net_haber_218_tiksindigim-meslegim-ve-eski-umutlarim", "r").read()
htmlparser = etree.HTMLParser()
tree = etree.HTML(file, htmlparser)

#$x('/html/body/div[2]/main/section[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/li[2]/span/a/span/text()')
#tree.xpath('//*[@id="haber-reklam"]/p/text()')
#'//li/span/a/span[@itemprop="title"]'
#'//li/span/a/span[@itemprop="title"]/text()'



# REAL URL

df = pd.DataFrame(columns=["filename", "category", "html", "text"])

l = []
filename = []
htmlfile = []
text = []

for elem in glob.glob("*"):
    print(elem)
    file = codecs.open(elem, "r").read()
    htmlparser = etree.HTMLParser()
    tree = etree.HTML(file, htmlparser)
    try:
        category = tree.xpath('//li/span/a/span[@itemprop="title"]/text()')[3]
        text = tree.xpath('//*[@id="haber-reklam"]//text()')
        if category == " İŞÇİ-SENDİKA":
            print("YES")
            serie = pd.Series([elem, category, file, text], index=df.columns)
            df = df.append(serie, ignore_index=True)
    except:
        l.append("Title is not included")
    l.append(category)
    
empty_docs = df.loc[df.text.str.len() == 0]


"""
for doc in empty_docs:
    html = doc.html
    htmlparser = etree.HTMLParser()
    tree = etree.HTML(file, htmlparser)
    try:
        try:
        category = tree.xpath('//li/span/a/span[@itemprop="title"]/text()')[3]
        text = tree.xpath('//*[@id="haber-reklam"]/p//text()')
        print(text)
        if category == " İŞÇİ-SENDİKA":
            print("YES")
            serie = pd.Series([elem, category, file, text], index=df.columns)
            empty_docs = df.append(serie, ignore_index=True)
    except:
        l.append("Title is not included")
    l.append(category)"""
    
    
json_text = []


links = df.filename.apply(lambda x: x.replace("___", "://"))
links = links.apply(lambda x: x.replace("_", "/"))


new_df = pd.DataFrame(columns = ["text", "link", "html", "text_sentences"])

new_df['text'] = df.text.apply(lambda x: " ".join(x))
new_df['link'] = links
new_df['html'] = df.html


all_json_lists = []
for elem in df['text']:
    json_obj_list = []
    if text:
        for sentence in elem:
            json_obj = {}
            json_obj['sentence_string'] = sentence
            json_obj_list.append(json_obj)
    else:
        json_obj = {}
        json_obj['sentence_string'] = ""
        json_obj_list.append(json_obj)
    
    all_json_lists.append(json_obj_list)
    #print(json_obj_list)

new_df['text_sentences'] = all_json_lists


list_json_articles = []
for idx, elem in new_df.iterrows():
    json_articles = {}
    json_articles['text'] = elem['text']
    json_articles['link'] = elem['link']
    json_articles['html'] = elem['html']
    json_articles['text_sentences'] = elem['text_sentences']
    list_json_articles.append(json_articles)
    
trying_list = []
trying_list = list_json_articles[0:20]

import json

batch1 = list_json_articles[0:100]
batch2 = list_json_articles[100:200]
batch3 = list_json_articles[200:300]
batch4 = list_json_articles[300:400]
batch5 = list_json_articles[400:]

with open('batch1.json', 'w') as f:
    f.write(json.dumps(batch1))
    
with open('batch2.json', 'w') as f:
    f.write(json.dumps(batch2))
    
with open('batch3.json', 'w') as f:
    f.write(json.dumps(batch3))
    
with open('batch4.json', 'w') as f:
    f.write(json.dumps(batch4))

with open('batch5.json', 'w') as f:
    f.write(json.dumps(batch5))
    
    
#new_df['text'] = all_text.loc[all_text.str.len() != 0]