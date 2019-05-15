import logging
import re
from urllib.parse import urlparse, urljoin, parse_qs
from corpus import Corpus
from lxml import etree
from io import BytesIO
import random

logger = logging.getLogger(__name__)

class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier):
        self.frontier = frontier
        self.corpus = Corpus()
        self.most_valid_links = tuple()
        self.valid_urls = []
        self.traps = []

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        f = open("analytics.txt","w+")
        f.write("SUBDOMAINS AND URLS PROCESSED\n")

        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.fetch_url(url)

            valid_links=0
            for next_link in self.extract_next_links(url_data,f):
                if self.corpus.get_file_name(next_link) is not None:
                    if self.is_valid(next_link):
                        self.frontier.add_url(next_link)
                        valid_links+=1
                        self.valid_urls.append(next_link)

            if not self.most_valid_links or valid_links>self.most_valid_links[1]:
                self.most_valid_links = (url,valid_links)

        
        f.write("\n\nMOST VALID LINKS\n")
        f.write("{0} contain the most valid links({1})".format(self.most_valid_links[0],self.most_valid_links[1]))
        f.write("\n\nDOWNLOADED URLS\n")
        for x in self.valid_urls:
            f.write(x + "\n")
        f.write("\n\nTRAPS\n")
        for t in self.traps:
            f.write(t + "\n")
        f.close()


    def fetch_url(self, url):
        """
        This method, using the given url, should find the corresponding file in the corpus and return a dictionary
        containing the url, content of the file in binary format and the content size in bytes
        :param url: the url to be fetched
        :return: a dictionary containing the url, content and the size of the content. If the url does not
        exist in the corpus, a dictionary with content set to None and size set to 0 can be returned.
        """
        url_data = {
            "url": url,
            "content": None,
            "size": 0
        }
        file_address = self.corpus.get_file_name(url)
        if file_address != None:
            f=open(file_address,"rb")
            url_data["content"]=f.read()
            url_data["size"]=len(url_data["content"])
            f.close
        return url_data

    def extract_next_links(self, url_data,f):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        outputLinks = []
        parser = etree.HTMLParser()
        tree=etree.parse(BytesIO(url_data["content"]),parser)
        paths = tree.xpath("//@href")
        for path in paths:
            if bool(urlparse(path).netloc):
                outputLinks.append(path)
            else:
                outputLinks.append(urljoin(url_data["url"],path))

        f.write("{0} contains {1} links\n".format(url_data["url"],len(outputLinks)))
        return outputLinks

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        if parsed.scheme == "http":
            if self.frontier.is_duplicate("https" + url[4:]):
                return False

        if parsed.scheme == "https":
            if self.frontier.is_duplicate("http" + url[5:]):
                return False

        if re.search(r"^.*?(/.+?/).*?\1.*\1.*\1.*\1.*\1.*\1.*\1.*\1.*\1.*$|^.*?/(.+?/)\2.*\2.*\2.*\2.*\2.*\2.*\2.*\2.*\2.*$", parsed.path):  #10 times /item/ in a path
            self.traps.append(url)
            return False

        if len(parsed.query)>0:
            queries = parse_qs(parsed.query)
            if self.frontier.similar(parsed.scheme + "://" + parsed.netloc + parsed.path,queries.keys()):
                self.traps.append(url)
                return False

        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

        except TypeError:
            print("TypeError for ", parsed)
            return False

