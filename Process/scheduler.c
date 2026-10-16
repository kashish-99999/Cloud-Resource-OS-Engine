#include <stdio.h>      // for printf
#include <stdlib.h>     // for rand()
#include "process.h"    // for Process struct and changeState()
#include "scheduler.h"
#include "fcfs.h"
#include "sjfs.h"
#include "srtf.h"
#include "priority.h"
#include "round_robin.h"

void simulateProcess(Process *p) {
    changeState(p, READY);
    if (rand() % 2) changeState(p, RUNNING);
    if (rand() % 2) changeState(p, WAITING);
    if (rand() % 2) changeState(p, SUSP_READY);
    if (rand() % 2) changeState(p, SUSP_WAITING);
    changeState(p, TERMINATED);
}

void runScheduler(AlgoType algo, Process processes[], int n, int quantum) {
    switch (algo) {
        case ALG_FCFS:
            printf("\n🔹 Using FCFS Scheduling Algorithm\n");
            fcfs(processes, n);
            break;
        case ALG_SJF:
            printf("\n🔹 Using SJF Scheduling Algorithm\n");
            sjf_np(processes, n);
            break;
        case ALG_SRTF:
            printf("\n🔹 Using SRTF Scheduling Algorithm\n");
            srtf(processes, n);
            break;
        case ALG_PRIORITY:
            printf("\n🔹 Using Priority Scheduling Algorithm\n");
            priority_np(processes, n);
            break;
        case ALG_ROUND_ROBIN:
            printf("\n🔹 Using Round Robin Scheduling Algorithm (Quantum = %d)\n", quantum);
            roundRobin(processes, n, quantum);
            break;
    }
}
