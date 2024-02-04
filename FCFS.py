from Task import task
import threading
import time
class myThread(threading.Thread):

    def __init__(self, name, event,mevent):
        threading.Thread.__init__(self)
        self.name = name
        self.state = 'idle'
        self.task = None
        self.event = event
        self.mevent=mevent

    def run(self):

        while True:
            self.event.wait()
            if self.task != None:
                if self.task.getRemainingTime() == 0:  # age task qabli tamum shode bendazash birun az cpu

                    self.state = 'idle'

                    threadLock.acquire()
                    available[0] += self.task.need[0]  # bargardoondane manabe
                    available[1] += self.task.need[1]
                    available[2] += self.task.need[2]
                    threadLock.release()
                    self.task = None
            if self.task == None:  # age taski dakhel cpu nist task vardare
                self.task, isempty = pull()

            if isempty == False or self.state == 'running':  # ejra kardane task
                self.state = 'running'
                self.task.doneTime += 1
            self.mevent.set()
            self.event.clear()



def pull() -> task:  # az ready queue task var midare
    threadLock.acquire()
    task=None
    while task==None :# search beshe baraye taski ke beshe dad be cpu tooye waiting ke momkene available satisfy nashe va bayad dobare search beshe
        if len(readyQueue)>0:
            task = readyQueue.pop(0)
            if available[0] >= task.need[0] and available[1] >= task.need[1] and available[2] >= task.need[2]:
                task.state = 'running'
                r1 = available.pop(0) - task.need[0]
                r2 = available.pop(0) - task.need[1]
                r3 = available.pop(0) - task.need[2]
                available.append(r1)
                available.append(r2)
                available.append(r3)
                isempty = False
            else:
                pushWaiting(task)
                task=None
        else: break

    if task==None:
        isempty = True
    threadLock.release()
    return task, isempty


def pushReady(task):  # append mikone be ready queue

    task.state = 'ready'
    readyQueue.append(task)



def pushWaiting(task):  # append mikone be  waiting queue
    task.state = 'waiting'
    waitingQueue.append(task)


threadLock = threading.Lock()

available = []  # resources
readyQueue = []
waitingQueue = []

# getting input
available = input().split()  # "enter resources amount"
taskAmount = input()  # "enter task amount"

for i in range(int(taskAmount)):
    name, Type, duration = input().split()
    readyQueue.append(task(name, int(duration), Type))
###
readyQueue = sorted(readyQueue, key=lambda x: x.priority)
available = [int(i) for i in available]

event1 = threading.Event()
mainEvent=threading.Event()
mainEvent2=threading.Event()
mainEvent3=threading.Event()
mainEvent4=threading.Event()

thread1 = myThread("CPU 1", event1,mainEvent)
thread2 = myThread("CPU 2", event1,mainEvent2)
thread3 = myThread("CPU 3", event1,mainEvent3)
thread4 = myThread("CPU 4", event1,mainEvent4)

threads=[thread1,thread2,thread3,thread4]

thread1.start()
thread2.start()
thread3.start()
thread4.start()
for timer in range(40):
    print("\nwe are in time " + str(timer))
    # if not event1.is_set():
    for i in range(3):
        print("R%s:%s " % (i + 1, available[i]), end='')

    print('\nReadyQueue: ', end='')
    if len(readyQueue) == 0:
        print("readyQueue is Empty!", end='')
    else:
        for i in readyQueue: print(i.name + ' ', end='')

    print('\nWaitingQueue: ', end='')
    if len(waitingQueue) == 0:
        print("waitingQueue is Empty!",end='')
    else:
        for i in waitingQueue:
            print(i.name+ ' ', end='')

    if thread1.state == 'running':
        print("\nCPU1 " + thread1.task.name)
    else:
        print("CPU1 " + thread1.state)

    if thread2.state == 'running':
        print("CPU2 " + thread2.task.name)
    else:
        print("CPU2 " + thread2.state)

    if thread3.state == 'running':
        print("CPU3 " + thread3.task.name)
    else:
        print("CPU3 " + thread3.state)

    if thread4.state == 'running':
        print("CPU4 " + thread4.task.name)
    else:
        print("CPU4 " + thread4.state)
    for i in waitingQueue:
        i.waitedTime += 1


    threadLock.acquire()
    for i in waitingQueue: #starvation
        if i.waitedTime > 4:
            task = waitingQueue.pop(waitingQueue.index(i))
            task.waitedTime=0
            pushReady(task)
    threadLock.release()
    event1.set()
    #time.sleep(3)
    for t in threads:
        t.mevent.wait()
        t.mevent.clear()

    if (len(waitingQueue) == 0 and len(readyQueue) == 0 and thread1.state == 'idle' and thread2.state == 'idle'
            and thread3.state == 'idle' and thread4.state == 'idle'): break

print("\nwe are in time " + str(timer+1))
# if not event1.is_set():
for i in range(3):
    print("R%s:%s " % (i + 1, available[i]), end='')

print('\nReadyQueue: ', end='')
if len(readyQueue) == 0:
    print("readyQueue is Empty!", end='')
else:
    for i in readyQueue: print(i.name + ' ', end='')

print('\nWaitingQueue: ', end='')
if len(waitingQueue) == 0:
    print("waitingQueue is Empty!")
else:
    for i in waitingQueue:
        print(i.name, end='')

if thread1.state == 'running':
    print("\nCPU1 " + thread1.task.name)
else:
    print("CPU1 " + thread1.state)

if thread2.state == 'running':
    print("CPU2 " + thread2.task.name)
else:
    print("CPU2 " + thread2.state)

if thread3.state == 'running':
    print("CPU3 " + thread3.task.name)
else:
    print("CPU3 " + thread3.state)

if thread4.state == 'running':
    print("CPU4 " + thread4.task.name)
else:
    print("CPU4 " + thread4.state)
# thread1.join()
# thread2.join()
# thread3.join()
# thread4.join()
print("Done main thread")
