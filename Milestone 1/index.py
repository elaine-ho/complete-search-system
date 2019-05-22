import json
import os
from HTMLparser import MyHTMLParser
import math
import re
from db import create_db

class Index:
    WEBPAGES_RAW_NAME = "WEBPAGES_RAW"
    JSON_FILE_NAME = os.path.join(".", WEBPAGES_RAW_NAME, "bookkeeping.json")

    def __init__(self):
        self.file_url_map = json.load(open(self.JSON_FILE_NAME), encoding="utf-8")
        self.url_file_map = dict()
        for key in self.file_url_map:
            self.url_file_map[self.file_url_map[key]] = key

        self.tf_idf={}
            
    def loop_urls(self):

        tf={}
        df=dict()

        for url in self.url_file_map:
            addr = self.url_file_map[url].split("/")
            dir = addr[0]
            file = addr[1]
            file_address = os.path.join(".", self.WEBPAGES_RAW_NAME, dir, file)
            parser = MyHTMLParser()
            f=open(file_address,"r",encoding="utf8")
            parser.feed(f.read())
            text = parser.get_data()

            tf[url]={}
            word_set = set()
            words=re.split("[^a-z0-9]+",text.lower())
            words=filter(None,words)
            for word in words:
                if not word in tf[url]:
                    tf[url][word] = 1
                else:
                    tf[url][word]+=1
                if not word in word_set:
                    if not word in df:
                        df[word]=1
                    else:
                        df[word]+=1
                    word_set.add(word)

            f.close()
        
        for doc in tf:
            for term in tf[doc]:
                if not term in self.tf_idf.keys():
                    self.tf_idf[term]={}
                self.tf_idf[term][doc]=(1+math.log(tf[doc][term],10)) * math.log(len(df)/df[term])

        create_db(self.tf_idf)

            