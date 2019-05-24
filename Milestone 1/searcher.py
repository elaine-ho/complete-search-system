from pymongo import MongoClient

class Searcher:
    def __init__(self,database):
        self.database=database

    def find(self,query):
        rankings=dict()

        words = query.lower().split()
        for word in set(words):
            myquery = {"term": word}
            url_score = self.database.find(myquery)

            duplicate_urls = set()
            if url_score.count()>0:
                for k,v in url_score[0]['URLs'].items():
                    if not k in duplicate_urls:
                        if not k in rankings:
                            rankings[k]=v
                        else:
                            rankings[k]+=v
                        duplicate_urls.add(k)
            
        sorted_rankings = sorted(rankings.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_rankings