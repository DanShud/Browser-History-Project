from webbrowser import Chrome
import browserhistoryAdjusted as bh

mydict = bh.write_browserhistory_csv(1000)



print(len(mydict["chrome"]))



