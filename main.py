import functions.browserhistoryAdjusted as bh
import re
from classes.browserObject import browserObject
# from functions.array   import mergeSort
import sqlite3
import functions.timeFrequency as timeFrequency 
from classes.graph import Graph
from functions.mostCommonWords import TopTwoWords
from functions.table import generateTable

HistoryPath = r"C:\Users\Kai\AppData\Local\Google\Chrome\User Data\Default\History"


""""""
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

"""reeading from google history
Uncomment it and delete history.db to use your history (if you have google history save in default)"""
mydict = bh.get_browserhistory(10000, HistoryPath)
 #print(mydict["chrome"][1])

myList= mydict["chrome"]
index = 0
for i in myList:
    # #print(i)
    url = re.sub("https://","",myList[100][0])
    if("www.google.com/search" in i[0] and ("www.google.com/maps" not in i[0])):  #filtering out non-google searchs (e.g www.youtube.com/code)
        cursor.execute("INSERT or IGNORE INTO tblHistory VALUES(?,?,?,?,?)",(i[0],i[1].split("- Google")[0],i[2],i[3],i[4]))
        conn.commit()
        index += 1
    if index > 1000:
        break


"""Grouping by word using hashing"""
graphDict = {}
cursor.execute("SELECT * FROM tblHistory") #this just gets everything from history.db as a list of tuples
myList = cursor.fetchall()

#opening and reading "blocklisted words" to an array 
# (at the moment only prepositions and articles are blocklisted to avoid arbitrary connections)
#credit to https://github.com/rali-udem/gophi/blob/master/lexical-data/prepositions.txt for the original list of prepositions
blocklist=  ""
with open("blocklist.txt",'r') as f:
    blocklist= f.readlines()
blocklist = [line[:-1] for line in blocklist]

count = 0 
for i in myList:
    # search = browserObject(i)
    for word in i[1].strip().split(" "):
        
        word = word.lower()
        if word not in blocklist or not word.isnumeric():
            if word not in graphDict:
                graphDict[word] = []
            equalto = False
            for j in graphDict[word]:
                if j == browserObject(i):
                    equalto = True
                    break
            if equalto == False:
                graphDict[word].append(browserObject(i))
            #print(browserObject(i))
            # #print(word)
            pass #occurs if word is in blocklist as it throws a keyError since it's not in the dictionary
#print(graphDict)


# creating graph

gp = Graph()


for i in graphDict:
    for j in range(len(graphDict[i])-1):
            gp.edge(graphDict[i][j], graphDict[i][j+1])

res = gp.grouping()

##print(res[0][1])

##print(timeFrequency.TimePeriod(res[0]))
##print(TopTwoWords(res[0]))

#print(res)
"""Creating list to add to table"""
tableList = []
for i in res:
    listOfLinks = []
    for j in i:
        #print("hi")
        listOfLinks.append(j.url)
    tableList.append((TopTwoWords(i), timeFrequency.TimePeriod(i), listOfLinks))


generateTable(tableList)