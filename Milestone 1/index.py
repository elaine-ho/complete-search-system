import json
import os
from HTMLparser import MyHTMLParser
import math
import re

class Index:
    WEBPAGES_RAW_NAME = "WEBPAGES_RAW"
    JSON_FILE_NAME = os.path.join(".", WEBPAGES_RAW_NAME, "bookkeeping.json")

    def __init__(self):
        self.file_url_map = json.load(open(self.JSON_FILE_NAME), encoding="utf-8")
        self.url_file_map = dict()
        for key in self.file_url_map:
            self.url_file_map[self.file_url_map[key]] = key
        self.tf={}
        self.df=dict()
        self.tf_idf={}
            
    def loop_urls(self):
        count = 0
        for url in self.url_file_map:
            if count > 10:
                break
            addr = self.url_file_map[url].split("/")
            dir = addr[0]
            file = addr[1]
            file_address = os.path.join(".", self.WEBPAGES_RAW_NAME, dir, file)
            parser = MyHTMLParser()
            f=open(file_address,"r",encoding="utf8")
            parser.feed(f.read())
            text = parser.get_data()
            self.tf[url]={}
            word_set = set()
            words=re.split("[^a-z0-9]+",text.lower())
            words=filter(None,words)
            for word in words:
                if not word in self.tf[url]:
                    self.tf[url][word] = 1
                else:
                    self.tf[url][word]+=1
                if not word in word_set:
                    if not word in self.df:
                        self.df[word]=1
                    else:
                        self.df[word]+=1
                    word_set.add(word)
            f.close()
            count+=1
        
        for doc in self.tf:
            for term in self.tf[doc]:
                if not term in self.tf_idf.keys():
                    self.tf_idf[term]={}
                self.tf_idf[term][doc]=(1+math.log(self.tf[doc][term],10)) * math.log(len(self.df)/self.df[term])

        with open('index.json', 'w') as outfile:
            json.dump(self.tf_idf, outfile, separators=('\n',': '))