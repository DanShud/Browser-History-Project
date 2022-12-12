from classes.browserObject import browserObject



#preconditions
#The input pf the fucntion TimePeriod is a lost of elemets, 
#the type of which is BrowserObject
def TimePeriod(link):
    if(len(link) == 1): #if list has only one element
        object = link[0]
        time = f'{object.getTime() // 60 }:{object.getTime() % 60}'
        return time
    else:
        #print("hello")
        lowerbound = 0
        upperbound = 24*60
        res = link
        while (len(res) > len(link) * 0.3) : #looking for the right diapason
            #print("helo")    
            bound = (lowerbound + upperbound) / 2
            left = []
            right = []
            U = 0
            L = 0
            for i in res:
                if i.getTime() < bound:
                    L += i.getVisitCount()
                    left.append(i)
                else:
                    U += i.getVisitCount()
                    right.append(i)
            if len(res) == 2:
                break
            identical = True
            for i in range(len(res)-1):
                if res[i].getTime() != res[i+1].getTime():
                    identical = False   
            if identical == True:
                return [f'{res[0].getTime() // 60 }:{str(res[0].getTime() % 60).zfill(2)}']
            else:
                if U > L:
                    lowerbound = bound
                    res = right
                else:
                    upperbound = bound
                    res = left
        mi = res[0]
        ma = res[0]
        
        for i in res:
            if i.getTime() < mi.getTime():
                mi = i
            if i.getTime() > mi.getTime():
                ma = i
        lefttime = f'{mi.getTime() // 60 }:{str(mi.getTime() % 60).zfill(2)}'
        righttime = f'{ma.getTime() // 60 }:{str(ma.getTime() % 60).zfill(2)}'
        return f"{lefttime}-{righttime}"
#postcondition
#function return sting in format xx:yy-xx:yy of the time period when the links
#from the list were searched the most often
