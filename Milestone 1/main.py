import os
from index import Index
from pymongo import MongoClient
from searcher import Searcher


if __name__ == "__main__":
    client = MongoClient(port=27017)
    if not 'CS121Project3' in client.list_database_names():
        Index().loop_urls(client)

    database = client["CS121Project3"]["ICSindex"]
    searcher = Searcher(database)

    is_searching = True
    while is_searching:
        query = input("Enter a query: ")
        while len(query)==0:
            query = input("Enter a valid query: ")

        ranked_results = searcher.find(query)

        count = 0
        for result in ranked_results:
            if count>20:
                break
            print(result[0])
            count+=1

        continue_search = input("Do you want to continue searching? (Y/N): ")
        while continue_search.lower()!="y":
            if continue_search.lower()=="n":
                is_searching=False
                break
            else:
                continue_search = input("Do you want to continue searching? (Y/N): ")
         
    
    
    