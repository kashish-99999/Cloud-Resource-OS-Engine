#ifndef SCHEDULER_H
#define SCHEDULER_H

#include "process.h"

typedef enum {
    ALG_FCFS,
    ALG_SJF,
    ALG_SRTF,
    ALG_PRIORITY,
    ALG_ROUND_ROBIN
} AlgoType;
void simulateProcess(Process *p);
void runScheduler(AlgoType algo, Process processes[], int n, int quantum);

#endif


