from Task import task
import time
available=[] #resources
readyQueue=[]
waitingQueue=[]
tasksQueue=[]
terminated=[] #terminated tasks

#getting input
available=input().split() #"enter resources amount"
taskAmount=input() #"enter task amount"

for i in range(int(taskAmount)):
    name,Type,duration=input().split()
    tasksQueue.append(task(name,int(duration),i,Type))

