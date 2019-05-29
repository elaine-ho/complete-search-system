import tkinter
from tkinter import *
from index import Index
from pymongo import MongoClient
from searcher import Searcher

def search_and_show():
    query = query_box.get()
    
    ranked_results = searcher.find(query)
    
    count = 0
    output = []
    for result in ranked_results:
        if count>20:
            break
        output.append(result)
        count+=1
    m.destroy()
    m.pack_forget()
    m.grid_forget()
    scrollbar = Scrollbar(m)
    scrollbar.pack(side = RIGHT, fill = Y)
    mylist = Listbox(m, yscrollcommand = scrollbar.set)
    for line in output:
        mylist.insert(END, str(line))
    mylist.pack( side = LEFT, fill = BOTH )
    scrollbar.config(command = mylist.yview)
    mainloop()
    
if __name__ == "__main__":
    client = MongoClient(port=27017)
    if not 'CS121Project3' in client.list_database_names():
        Index().loop_urls(client)

    database = client["CS121Project3"]["ICSindex"]
    searcher = Searcher(database)
    
    m = tkinter.Tk()
    Label(m, text='Enter a query:').grid(row=0)
    query_box = Entry(m)
    submit_button = Button(m, text="Search", command=search_and_show)
    query_box.pack(side = LEFT, fill = BOTH)
    submit_button.pack(side = LEFT, fill = BOTH)
    m.mainloop()