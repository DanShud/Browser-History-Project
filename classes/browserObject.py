

class browserObject():
    

    #passing sqlquery and making an object, allowing us to access data more easily
    def __init__(self, SqlQuery:list):
        """
        Precondition
        len(SqlQuery) == 5 
        type(SqlQuery[2]) == type(2) 
        """
        self.url = SqlQuery[0].strip()
        self.title = SqlQuery[1].strip().lower()
        self.visitCount = SqlQuery[2]

        #converting date time to minutes
        tempdate = SqlQuery[4]
        #format is date/month/year hour:minute:second
        tempdate = (int(tempdate.split(" ")[1].split(":")[0])*60) + int(tempdate.split(" ")[1].split(":")[1]) 

        """Post Condition for date conversion:
            tempdate//60 == tempdate.split(" ")[1].split(":")[0]
            and
            tempdate%60 == tempdate.split(" ")[1].split(":")[1]
        """
        # print(tempdate)
        self.lastVisitDate = tempdate


    """Accessors"""

    def getTime(self):
        return self.lastVisitDate

    def getTitle(self):
        return self.title

    def getVisitCount(self):
        return self.visitCount

    def __str__(self):
        return self.title

    def __equal__(self, other):
        return self.title == other.getTitle()