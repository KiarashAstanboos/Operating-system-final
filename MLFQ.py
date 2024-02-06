from Task import task
import threading
import time
from queue import PriorityQueue


class myThread(threading.Thread):

    def __init__(self, name, event, mevent):
        threading.Thread.__init__(self)
        self.name = name
        self.state = 'idle'
        self.task = None
        self.event = event
        self.mevent = mevent
        self.timer = 0

    def run(self):

        while True:
            self.event.wait()
            if self.task != None:
                if self.task.getRemainingTime() == 0 or self.timer == self.task.mlfq:  # age task qabli tamum shode ya Q tamum shode bendazash birun az cpu

                    self.state = 'idle'

                    threadLock.acquire()

                    available[0] += self.task.need[0]  # bargardoondane manabe
                    available[1] += self.task.need[1]
                    available[2] += self.task.need[2]
                    if self.task.getRemainingTime() == 0: terminated.append(self.task)

                    if self.timer == self.task.mlfq and self.task.getRemainingTime() != 0:

                        if self.task.mlfq == Q2:  # andakhtan too q3
                            self.task.mlfq = Q3
                            self.task.state = 'ready'
                            Queue3.append(self.task)  # andakhtan too q2
                        elif self.task.mlfq == Q1:
                            self.task.mlfq = Q2
                            self.task.state = 'ready'
                            Queue2.append(self.task)
                    self.timer = 0
                    threadLock.release()
                    self.task = None

            if self.task == None:  # age taski dakhel cpu nist task vardare
                self.task, isempty = pull()

            if isempty == False or self.state == 'running':  # ejra kardane task
                self.state = 'running'
                self.task.doneTime += 1
                self.timer += 1
            self.event.clear()
            self.mevent.set()


def pull() -> task:  # az  queue task var midare
    threadLock.acquire()
    task = None
    while task == None:  # search beshe baraye taski ke beshe dad be cpu tooye waiting ke momkene available satisfy nashe va bayad dobare search beshe
        if len(Queue1) > 0:
            while len(Queue1) > 0:  # Q1
                task = Queue1.pop(0)
                if available[0] >= task.need[0] and available[1] >= task.need[1] and available[2] >= task.need[2]:
                    task.state = 'running'
                    r1 = available.pop(0) - task.need[0]
                    r2 = available.pop(0) - task.need[1]
                    r3 = available.pop(0) - task.need[2]
                    available.append(r1)
                    available.append(r2)
                    available.append(r3)
                    task.mlfq = Q1
                    isempty = False
                    break
                else:
                    Queue2.append(task)
                    task = None
        elif len(Queue2) > 0 :
            while len(Queue2) > 0:  # Q2
                task = Queue2.pop(0)
                if available[0] >= task.need[0] and available[1] >= task.need[1] and available[2] >= task.need[2]:
                    task.state = 'running'
                    r1 = available.pop(0) - task.need[0]
                    r2 = available.pop(0) - task.need[1]
                    r3 = available.pop(0) - task.need[2]
                    available.append(r1)
                    available.append(r2)
                    available.append(r3)
                    task.mlfq = Q2
                    isempty = False
                    break
                else:
                    Queue3.append(task)
                    task = None
        elif len(Queue3) > 0 :
            i = 0
            while len(Queue3) > i:  # Q3
                task = Queue3.pop(0)
                if available[0] >= task.need[0] and available[1] >= task.need[1] and available[2] >= task.need[2]:
                    task.state = 'running'
                    r1 = available.pop(0) - task.need[0]
                    r2 = available.pop(0) - task.need[1]
                    r3 = available.pop(0) - task.need[2]
                    available.append(r1)
                    available.append(r2)
                    available.append(r3)
                    task.mlfq = Q3
                    isempty = False
                    break
                else:
                    Queue3.append(task)
                    task = None
                    i += 1
            if task == None:
                break
    if task == None:
        isempty = True
    threadLock.release()
    return task, isempty


threadLock = threading.Lock()

available = []  # resources
Queue1 = []
Queue2 = []
Queue3 = []

terminated = []
Q1 = 2
Q2 = 4
Q3 = 1000

# getting input
available = input().split()  # "enter resources amount"
taskAmount = input()  # "enter task amount"

for i in range(int(taskAmount)):
    name, Type, duration = input().split()
    temp = task(name, int(duration), Type)
    temp.mlfq = Q1
    if temp.burst > 0:
        Queue1.append(temp)
###
Queue1 = sorted(Queue1, key=lambda x: x.priority)
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

    print('\nQ1: ', end='')
    if len(Queue1) == 0:
        print("Q1 is Empty!", end='')
    else:
        for i in Queue1: print(i.name + ' ', end='')

    print('\nQ2: ', end='')
    if len(Queue2) == 0:
        print("Q2 is Empty!", end='')
    else:
        for i in Queue2:
            print(i.name + ' ', end='')

    print('\nQ3: ', end='')
    if len(Queue3) == 0:
        print("Q3 is Empty!", end='')
    else:
        for i in Queue3: print(i.name + ' ', end='')
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

    event1.set()
    # time.sleep(3)
    for t in threads:
        t.mevent.wait()
        t.mevent.clear()

    if (len(Queue1) == 0 and len(Queue2) == 0 and len(
            Queue3) == 0 and thread1.state == 'idle' and thread2.state == 'idle'
            and thread3.state == 'idle' and thread4.state == 'idle'): break
    timer += 1
print("\nwe are in time " + str(timer + 1))
# if not event1.is_set():
for i in range(3):
    print("R%s:%s " % (i + 1, available[i]), end='')

print('\nQ1: ', end='')
if len(Queue1) == 0:
    print("Q1 is Empty!", end='')
else:
    for i in Queue1: print(i.name + ' ', end='')

print('\nQ2: ', end='')
if len(Queue2) == 0:
    print("Q2 is Empty!", end='')
else:
    for i in Queue2:
        print(i.name + ' ', end='')

print('\nQ3: ', end='')
if len(Queue3) == 0:
    print("Q3 is Empty!", end='')
else:
    for i in Queue3: print(i.name + ' ', end='')
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
