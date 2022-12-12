“Browser history examiner” is a program that examines recent google searches, separates them into groups by the same category, and finds the time period of the most active users of those gropes. The output of the program is represented as an external table. It was developed as the final project for Introduction to Computer Science and Data Structures by Kai Britt and Dan Shudrenko.
How to run it?
Change the value of the variable “HistoryPath” to the actual path to the history file in “main.py”, and then run the file. 
How we did it. 
Firstly, the program puts the browser history in the SQL database for future analysis using the module “browserhistory”. The module “browserhistory” was adjusted, and the respective code may be found in the file “broserhistoryadjuted.py”.
Secondly, we developed the “browserobject”, which may be found in “broserobject.py,” to store the URL, time, title, and visit count, and then we hashed all the objects by common words. 
Then, we developed a graph object and constructed the graph, in which the nodes were broswerobject elements, and edges meant that the two nodes had words in common. To the object graph, we added the method “grouping,” with the algorithm based on DFS, to find the compound of the graph and separate them into different groups. The code for the object and the method may be found in “Graph.py”.
The next step was developing the function “TimePeriod”, which may be found in “TimeFrequency.py”. The function found the time period in which 30% of the ceratin group search happened.
Finally, we used “tkinter” module to present the data collected as the table. The code may be found in the “Table.py” file.
