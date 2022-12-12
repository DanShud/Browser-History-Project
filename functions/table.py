  
from tkinter import *

from  tkinter import ttk


def generateTable(tableData):
    """
    Pre Condition:
    TableData must be of type List, 
    TableData[0] must be of type Tuple and have a length of Three
    (Could iterate through all of table data but this might become an issue when table data becomes too large)
    """

    ws  = Tk()
    ws.title('Browser Data')
    print(f'1920x1080')
    ws.geometry(f'1920x260')
    ws['bg'] = '#000000'

    table_frame = Frame(ws)
    table_frame.config(width=1920, height=520)
    table_frame.pack(fill='both')

#scrollbar taken from tutorialpoint
    table_scroll1 = Scrollbar(table_frame)
    table_scroll1.pack(side=RIGHT, fill='y')

    table_scroll = Scrollbar(table_frame,orient= 'horizontal')
    table_scroll.pack(side= BOTTOM,fill='x')

    myTable = ttk.Treeview(table_frame,yscrollcommand=table_scroll1.set, xscrollcommand =table_scroll.set)
    
    
    #adding tree view to table_frame, tried to make it scale with both x and y couldn't figure it out :()
    myTable.pack(fill='both')

    table_scroll.config(command=myTable.yview)
    table_scroll.config(command=myTable.xview)

 
    myTable['columns'] = ('Groups', 'Times', 'Links') #making column headings

    """Frommatting columns"""
    myTable.column("#0", width=0,  stretch=NO)
    myTable.column("Groups",anchor=CENTER, width=60)
    myTable.column("Times",anchor=CENTER,width=20)
    myTable.column("Links",anchor=CENTER,width=480)
    myTable.rowconfigure(0,minsize=60)

#Create Headings 
    myTable.heading("#0",text="",anchor=CENTER)
    myTable.heading("Groups",text="group",anchor=CENTER)
    myTable.heading("Times",text="time",anchor=CENTER)
    myTable.heading("Links",text="links", anchor=CENTER)


#add data 
    DuplicateDict = {}
    for index,i in enumerate(tableData):
        if i[0] in DuplicateDict:
            pass
        else:
            myTable.insert(parent='',index='end',iid=index ,text='', values=i)
            DuplicateDict[i[0]] = "in"

    myTable.pack(fill='both')


    ws.mainloop()

