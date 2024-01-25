from Task import task
import threading
import time


class myThread(threading.Thread):

    def __init__(self, name, event):
        threading.Thread.__init__(self)
        self.name = name
        self.state = 'idle'
        self.task = None
        self.event = event

    def run(self):

            # self.event.wait()
            # if self.state == 'idle':
            self.task = pull()
            self.state = 'running'
            if self.state=='running':
                process(self.event,self.name,self.task,self.state)
                # self.task.doneTime += 1
                # with printLock:
                #     printState(self.state, self.task, self.name)
            # self.event.clear()
def process(event,name,task,state):
    while not event.is_set():
        event.wait()
        if task.getRemainingTime() <= 0:
            state = 'idle'
            task=None
        else:task.doneTime += 1
        with printLock:
            printState(state, task, name)

        event.clear()


def printState(state, task, name):
    # if name == 'CPU 1':
    #     print('\n')
    #     for i in range(3):
    #         print(" R%s: %s " % (i + 1, available[i]), end='')
    #
    #     print('\nReadyQueue: ', end='')
    #     if len(readyQueue) == 0:
    #         print("readyQueue is Empty!")
    #     else:
    #         for i in readyQueue: print(i.name + ' ', end='')
    #
    #     print('\nWaitingQueue: ', end='')
    #     if len(waitingQueue) == 0:
    #         print("waitingQueue is Empty!")
    #     else:
    #         for i in waitingQueue:
    #             print(i.name, end='')
    if state == 'idle':
        print("%s: %s \n" % (name, state))
    else:
        print("%s: %s %s\n" % (name, state, task.name))



def pull() -> task:  # az ready queue task var midare
    threadLock.acquire()
    task = readyQueue.pop(0)
    task.state = 'running'
    r1 = available.pop(0) - task.need[0]
    r2 = available.pop(0) - task.need[1]
    r3 = available.pop(0) - task.need[2]

    available.append(r1)
    available.append(r2)
    available.append(r3)
    threadLock.release()

    return task


def pushReady(self, task):  # append mikone be ready queue
    task.state = 'ready'
    readyQueue.append(task)


def pushWaiting(task):  # append mikone be  waiting queue
    task.state = 'waiting'
    waitingQueue.append(task)


threadLock = threading.Lock()
printLock=threading.Lock()

available = []  # resources
readyQueue = []
waitingQueue = []
tasksQueue = []
terminated = []  # terminated tasks

# getting input
available = input().split()  # "enter resources amount"
taskAmount = input()  # "enter task amount"

for i in range(int(taskAmount)):
    name, Type, duration = input().split()
    readyQueue.append(task(name, int(duration), i, Type))
###

available = [int(i) for i in available]

event1 = threading.Event()
# event2 = threading.Event()
# event3 = threading.Event()
# event4 = threading.Event()

thread1 = myThread("CPU 1", event1)
thread2 = myThread("CPU 2", event1)
thread3 = myThread("CPU 3", event1)
thread4 = myThread("CPU 4", event1)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
for i in range(7):
    with printLock:
    # if not event1.is_set():
        print('\n')
        for i in range(3):
            print("R%s:%s " % (i + 1, available[i]), end='')

        print('\nReadyQueue: ', end='')
        if len(readyQueue) == 0:
            print("readyQueue is Empty!")
        else:
            for i in readyQueue: print(i.name + ' ', end='')

        print('\nWaitingQueue: ', end='')
        if len(waitingQueue) == 0:
            print("waitingQueue is Empty!")
        else:
            for i in waitingQueue:
                print(i.name, end='')

    event1.set()
    # event2.set()
    # event3.set()
    # event4.set()
    time.sleep(3)
thread1.join()
thread2.join()
thread3.join()
thread4.join()
print("Done main thread")
