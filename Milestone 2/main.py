import tkinter
from tkinter import *
from index import Index
from pymongo import MongoClient
from searcher import Searcher

def search_and_show():
    query = query_box.get()
    
    ranked_results = searcher.find(query)
    
    output = []
    for result in ranked_results:
        output.append(result[0])
    scrollbar = Scrollbar(m)
    scrollbar.pack(side = RIGHT, fill = Y)
    mylist = Listbox(m, yscrollcommand = scrollbar.set)
    for line in output:
        mylist.insert(END, str(line))
    mylist.pack( side = TOP, fill = BOTH )
    scrollbar.config(command = mylist.yview)
    mainloop()
    

if __name__ == "__main__":
    client = MongoClient(port=27017)
    if not 'CS121Project3' in client.list_database_names():
        Index().loop_urls(client)

    database = client["CS121Project3"]
    searcher = Searcher(database)
    
    m = tkinter.Tk()
    Label(m, text='Enter a query:').pack(side=TOP, fill=BOTH)
    query_box = Entry(m)
    submit_button = Button(m, text="Search", command=search_and_show)
    query_box.pack(side = TOP, fill = BOTH)
    submit_button.pack(side = TOP, fill = BOTH)
    m.mainloop()