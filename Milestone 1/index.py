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


    def get_file_address(self,url):
        addr = self.url_file_map[url].split("/")
        dir = addr[0]
        file = addr[1]
        return os.path.join(".", self.WEBPAGES_RAW_NAME, dir, file)
    
            
    def loop_urls(self,client):

        tf={}
        df=dict()
        important_tags = dict()

        for url in self.url_file_map:
            file_address = self.get_file_address(url)
            f=open(file_address,"r",encoding="utf8")

            parser = MyHTMLParser()
            parser.feed(f.read())
            text = parser.get_data()

            tf[url]={}
            word_set = set() #for df

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

            important_tags[url]=parser.get_important_words()
            f.close()
        
        for doc in tf:
            for term in tf[doc]:
                if not term in self.tf_idf.keys():
                    self.tf_idf[term]={}
                self.tf_idf[term][doc]=(1+math.log(tf[doc][term],10)) * math.log(len(df)/df[term])

                if term in important_tags[doc]["h1"]:
                    self.tf_idf[term][doc]+=3
                elif term in important_tags[doc]["bold"]:
                    self.tf_idf[term][doc]+=2
                elif term in important_tags[doc]["h2"]:
                    self.tf_idf[term][doc]+=1
                elif term in important_tags[doc]["h3"]:
                    self.tf_idf[term][doc]+=.5

        create_db(client,self.tf_idf)

            