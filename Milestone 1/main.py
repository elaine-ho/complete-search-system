import os
from index import Index

if __name__ == "__main__":
    index_exists = os.path.isfile('index.json')
    if not index_exists:
        index=Index()
        index.loop_urls()
    
    