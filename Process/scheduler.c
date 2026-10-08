#include "process.h"
#include <stdio.h>
#include <stdlib.h>

#define MAX_QUEUE 10

PCB *readyQueue[MAX_QUEUE];
int rq_front = 0, rq_rear = 0;

void enqueueReady(PCB *p) {
    readyQueue[rq_rear++] = p;
    printf("Process %d entered READY queue\n", p->pid);
}

PCB* dequeueReady() {
    if (rq_front == rq_rear) return NULL;
    return readyQueue[rq_front++];
}

void runScheduler() {
    PCB *p;
    while ((p = dequeueReady()) != NULL) {
        dispatchProcess(p);
        while (p->remaining_time > 0) {
            p->remaining_time--;
            p->progress = ((float)(p->burst_time - p->remaining_time) / p->burst_time) * 100;
            printf("Process %d running... %0.2f%% complete\n", p->pid, p->progress);
        }
        terminateProcess(p);
    }
}
