# Task Scheduling Algorithms Overview

This repository provides implementations of various task scheduling algorithms for operating systems. Each algorithm aims to efficiently allocate resources and manage task execution based on different criteria.

## First Come First Serve (FCFS)

Tasks are sorted by their priority before execution begins. For each task, the algorithm checks resource availability. If resources are not available, the task is pushed to the waiting queue; otherwise, it is assigned to a CPU. Starvation is prevented by prioritizing tasks based on their priority or remaining time compared to tasks in the ready queue. Aging increases the priority of tasks in the waiting queue over time.

## Shortest Job First (SJF)

Similar to FCFS, tasks are sorted, but based on their burst times. If burst times are equal, priorities are used as tiebreakers.

## Round Robin (RR)

Tasks are executed in a cyclic manner, with each task getting a quantum of CPU time. Tasks are pushed out of the CPU upon reaching the time quantum or upon termination.

## Multilevel Feedback Queue (MLFQ)

Similar to RR, but with multiple queues for tasks. Tasks move between queues based on resource availability and execution time. Each queue has its own quantum time.

## Highest Response Ratio Next (HRRN)

Tasks are scheduled based on their response ratio, which considers waiting time and burst time. Tasks with higher response ratios are given priority.

## Synchronization

Shared memory access, such as queues, is synchronized using locks to ensure thread safety. Communication between CPUs and the main thread is facilitated by events, with CPUs signaling the main thread upon job completion and the main thread signaling CPUs to execute tasks.

## How to Use

1. Clone the repository to your local machine.
2. Compile and run the provided code for each scheduling algorithm.
3. Adjust parameters such as quantum time or queue settings as needed.
4. Analyze the performance and behavior of each algorithm.

## Contribution

Contributions are welcome! Feel free to submit issues or pull requests to improve the implementations or add new scheduling algorithms.

## License

This project is licensed under the [MIT License](LICENSE).
