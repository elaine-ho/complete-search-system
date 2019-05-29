from html.parser import HTMLParser
import json
import re

class MyHTMLParser(HTMLParser): # From https://docs.python.org/3/library/html.parser.html
    def __init__(self):
        super().__init__()
        self.reset()
        self.tag = None
        self.is_in_body = False
        self.data = []
        self.important_data = {
            "h1":set(),
            "h2": set(),
            "h3": set(),
            "b": set(),
            "strong" : set()
        }

    def handle_starttag(self, tag, attrs):
        self.tag=tag
        if tag == "body":
            self.is_in_body=True

    def handle_endtag(self, tag):
        self.tag = None
        if tag == "body":
            self.is_in_body=False

    def handle_data(self, d):
        if self.is_in_body and self.tag!="script":
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