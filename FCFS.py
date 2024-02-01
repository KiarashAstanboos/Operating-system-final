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
        self.task = pull()
        self.state = 'running'
        while True:
            self.event.wait()
            if self.state == 'running':
                if self.task.getRemainingTime() <= 0:
                    self.state = 'idle'
                    self.task = None
                else:
                    self.task.doneTime += 1
            self.event.clear()






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
printLock = threading.Lock()

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

available = [int(i) for i in available]

event1 = threading.Event()

thread1 = myThread("CPU 1", event1)
thread2 = myThread("CPU 2", event1)
thread3 = myThread("CPU 3", event1)
thread4 = myThread("CPU 4", event1)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
for i in range(7):

    print('\n')
    print("we are in time "+str(i))
    # if not event1.is_set():
    for i in range(3):
        print("R%s:%s " % (i + 1, available[i]), end='')

    print('\nReadyQueue: ', end='')
    if len(readyQueue) == 0:
        print("readyQueue is Empty!")
    else:
        for i in readyQueue: print(i.name + ' ', end='')

    print('WaitingQueue: ', end='')
    if len(waitingQueue) == 0:
        print("waitingQueue is Empty!")
    else:
        for i in waitingQueue:
            print(i.name, end='')

    if thread1.state == 'running':
        print("CPU1 " + thread1.task.name)
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
    event1.set()

    time.sleep(3) #event.wait()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
print("Done main thread")
