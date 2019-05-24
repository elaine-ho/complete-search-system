from html.parser import HTMLParser
import json
import re

class MyHTMLParser(HTMLParser): # From https://docs.python.org/3/library/html.parser.html
    def __init__(self):
        super().__init__()
        self.reset()
        self.tag = None
        self.handle = [False,None] # [0] reports if data will be handled [1] is the starting tag (if in self.tags)
        self.data = []
        self.tags = ["title","h1","h2","h3","h4","h5","h6","p","table","li"]
        self.important_data = {
            "h1":set(),
            "h2": set(),
            "h3": set(),
            "bold": set()
        }

    def handle_starttag(self, tag, attrs):
        self.tag=tag
        if tag in self.tags:
            self.handle[0]=True
            self.handle[1]=tag

    def handle_endtag(self, tag):
        self.tag = None
        if tag == self.handle[1]:
            self.handle[0]=False
            self.handle[1]=None

    def handle_data(self, d):
        if self.handle[0]:
            self.data.append(d)

        words=re.split("[^a-z0-9]+",d.lower())
        words=filter(None,words)
        for key in self.important_data:
            if self.tag==key:
                self.important_data[key].union(set(words))

    def get_data(self):
        return ' '.join(self.data)

    def get_important_words(self):
        return self.important_data