from Task import task
import threading
import time


class myThread(threading.Thread):

    def __init__(self, name, event, mevent):
        threading.Thread.__init__(self)
        self.name = name
        self.state = 'idle'
        self.task = None
        self.event = event
        self.mevent = mevent

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
                    terminated.append(self.task)

                    if len(waitingQueue) > 0:  # starvation
                        # check kardan bar asase priority
                        if len(readyQueue) > 4:
                            if (waitingQueue[0].priority < readyQueue[0].priority or
                                    waitingQueue[0].priority < readyQueue[1].priority or
                                    waitingQueue[0].priority < readyQueue[2].priority or
                                    waitingQueue[0].priority < readyQueue[3].priority):  # starvation
                                tempp = waitingQueue.pop(0)
                                readyQueue.insert(0, tempp)

                            # check kardan bar asase remaining time
                            if (waitingQueue[0].getRemainingTime() < readyQueue[0].getRemainingTime() or
                                    waitingQueue[0].getRemainingTime() < readyQueue[1].getRemainingTime() or
                                    waitingQueue[0].getRemainingTime() < readyQueue[2].getRemainingTime() or
                                    waitingQueue[0].getRemainingTime() < readyQueue[3].getRemainingTime()):  # starvation
                                tempp = waitingQueue.pop(0)
                                readyQueue.insert(0, tempp)
                        # check kardan bar asase manabe mojud
                        else:
                            for i in waitingQueue:
                                if canget(i):
                                    tempp = waitingQueue.pop(waitingQueue.index(i))
                                    tempp.state = 'ready'
                                    readyQueue.insert(0, tempp)

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
    task = None
    while task == None:  # search beshe baraye taski ke beshe dad be cpu tooye waiting ke momkene available satisfy nashe va bayad dobare search beshe
        if len(readyQueue) > 0:
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
                task = None
        else:
            break

    if task == None:
        isempty = True
    threadLock.release()
    return task, isempty

def canget(task):
    if task.need[0] <= available[0] and task.need[1] <= available[1] and task.need[2] <= available[2]:
        return True
    else:
        return False
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
terminated = []

# getting input
available = input().split()  # "enter resources amount"
taskAmount = input()  # "enter task amount"

for i in range(int(taskAmount)):
    name, Type, duration = input().split()
    temp = task(name, int(duration), Type)
    if temp.burst > 0:
        readyQueue.append(temp)
###
readyQueue = sorted(readyQueue, key=lambda x: x.priority)
available = [int(i) for i in available]

event1 = threading.Event()

mainEvent = threading.Event()
mainEvent2 = threading.Event()
mainEvent3 = threading.Event()
mainEvent4 = threading.Event()

thread1 = myThread("CPU 1", event1, mainEvent)
thread2 = myThread("CPU 2", event1, mainEvent2)
thread3 = myThread("CPU 3", event1, mainEvent3)
thread4 = myThread("CPU 4", event1, mainEvent4)

threads = [thread1, thread2, thread3, thread4]

thread1.start()
thread2.start()
thread3.start()
thread4.start()
timer = 0
while True:
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
        print("waitingQueue is Empty!", end='')
    else:
        for i in waitingQueue:
            print(i.name + ' ', end='')

    print('\nTerminated: ', end='')
    if len(terminated) == 0:
        print("Terminated is Empty!", end='')
    else:
        for i in terminated:
            print(i.name + ' ', end='')

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

    threadLock.acquire()
    for i in waitingQueue:
        i.waitedTime += 1
    for i in readyQueue:
        i.waitedTime += 1

    for i in waitingQueue:  # aging
        if i.waitedTime % 4 == 0: i.priority -= 1  # har 4 vahed zamani be priority ezafe mishe
    sorted(waitingQueue, key=lambda x: (x.priority,x.getRemainingTime()))  # sort kardane priority Queue
    sorted(readyQueue, key=lambda x: (x.getHRRN(),x.priority),reverse=True)

    threadLock.release()
    event1.set()
    # time.sleep(3)
    for t in threads:  # sabr kardan baraye thread ha ke tamum beshe kareshun
        t.mevent.wait()
        t.mevent.clear()

    if (len(waitingQueue) == 0 and len(readyQueue) == 0 and thread1.state == 'idle' and thread2.state == 'idle'
            and thread3.state == 'idle' and thread4.state == 'idle'): break
    if (len(readyQueue) == 0 and thread1.state == 'idle' and thread2.state == 'idle'
            and thread3.state == 'idle' and thread4.state == 'idle'):
        flag=False
        for i in waitingQueue:
            if canget(i):flag=True
        if flag==False: break
    timer += 1

print("\nwe are in time " + str(timer + 1))
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

print('\nTerminated: ', end='')
if len(terminated) == 0:
    print("Terminated is Empty!", end='')
else:
    for i in terminated:
        print(i.name + ' ', end='')

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
