from classes.browserObject import browserObject

#input is a list of browser objects
with open("blocklist.txt",'r') as f:
    blocklist= f.readlines()
blocklist = [line[:-1] for line in blocklist] #removing \n at the end of the string


def TopTwoWords(myList):
    """
    precondition:
    type(myList) == type([])
    isinstance(myList[0], browserObject)

    """
    outputDict = {}

    for i in myList:
        # sentence = i.getTitle()
        for j in i.getTitle().split(" "): #splitting since input is a sentence
            #print(j)
            if j not in blocklist and not j.isnumeric(): #only procced if it is not a number, or in the blocklist
                if j not in outputDict:        
                    outputDict[j] = 1*i.getVisitCount()  #multiplying by visit count to create weight based on the number of times the page has been visited
                else:
                    outputDict[j] += outputDict[j] + 1*i.getVisitCount()
            else:
                pass
    #print(outputDict)
    max1 = max(outputDict, key=outputDict.get) #get the key of the maximum value
    #print(max1)
    outputDict[max1] = 0
    max2 = max(outputDict, key=outputDict.get) #get the key of the new maximum
    #print("hello")
    return str(f'{max1}, {max2}')
            


