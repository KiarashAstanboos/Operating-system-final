FCFS:
sorting tasks by their priority before begining the execution.
for each task the algorithm checks either we have the resources or not. if the resources are not available the task will get pushed to the waiting queue other wise the task wil be asigned to a cpu.(in pull function)
starvation: after each time a task is terminated, the algorithm checks if the first task of the waiting queue has higher priority or less remaining time than first 3 tasks of readyQueue, it will push the task to the readyQueue
Aging: after each 4 clock that the task has been in the waitingQueue, the task's priority will get increased and after each clock the waiting queue will get sorted by the priorities so it is a priority queue.

SJF: same as FCFS but the tasks will get sorted by their burst times (if burst times are same the taks will get sorted by their prioriteis as a tiebraker).

RR: same as two algorithms before but the condition for pushing tasks away from the cpu is reaching the desired time quantum or getting terminated.set the self.Q in the myTHread for custom quantum time.

MLFQ: same as before but there is no waiting queue so if any tasks cant get desired recourses, it will get pushed to the next queue.set Q1,Q2,Q3 for custom quantum time for each queue.

HRRN: same as FCFS but tasks waited time will increase even they are in the ready queue. after each iteration the ready will get sorted by the value of getHRRN().


Synchronization: for shared memories like Queue, if any cpu wants to write or read from it, it will acquire and release the lock.
for communications between cpus i've used 5 events. 4 events for cpus to event the main thread that they have finished their job so the main thread can go to the next iteration and 1 event so the main thread can tells cpus to execute the task.
