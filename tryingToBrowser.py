from webbrowser import Chrome
import browserhistoryAdjusted as bh
import re
# from functions.array   import mergeSort
import sqlite3
mydict = bh.get_browserhistory(10000)

from graph import Graph
# print(mydict["chrome"][1])

myList= mydict["chrome"]


conn = sqlite3.connect("history.db") 
cursor = conn.cursor()  

createTable = """CREATE TABLE IF NOT EXISTS tblHistory(
                url TEXT PRIMARY KEY,
                title TEXT,
                visit_count INTEGER NOT NULL,
                type_count INTEGER NOT NULL,
                last_visit TEXT NOT NULL)"""

cursor.execute(createTable)
conn.commit()

index = 0
for i in myList:
    # print(i)
    url = re.sub("https://","",myList[100][0])
    if("www.google.com" in i[0]):  #filtering out non-google searchs (e.g www.youtube.com/code)
        cursor.execute("INSERT or IGNORE INTO tblHistory VALUES(?,?,?,?,?)",(i[0],i[1].split("- Google")[0],i[2],i[3],i[4]))
        conn.commit()
        index += 1
    if index > 1000:
        break


#dictionary stuff
newDict = {}
cursor.execute("SELECT * FROM tblHistory")
myList = cursor.fetchall()
#print(myList[0],myList[1],myList[2])


for i in myList:
    for word in i[1].strip().split(" "):
        if word not in newDict:
            newDict[word] = []
        newDict[word].append(i[1])
#print(newDict)


# creating graph

gp = Graph()

for i in newDict:
    for j in range(len(newDict[i])-1):
        gp.edge(newDict[i][j], newDict[i][j+1])

res = gp.grouping()

print(res)