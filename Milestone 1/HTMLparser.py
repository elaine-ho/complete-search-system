from html.parser import HTMLParser

class MyHTMLParser(HTMLParser): # From https://docs.python.org/3/library/html.parser.html
    def __init__(self):
        super().__init__()
        self.reset()
        self.tag = None
        self.handle = [False,None]
        self.data = []
        self.tags = ["title","h1","h2","h3","h4","h5","h6","p","table","li"]

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

    def get_data(self):
        return ' '.join(self.data)