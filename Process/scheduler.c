#include "process.h"
#include <stdio.h>
#include <stdlib.h>

#define MAX_QUEUE 10

PCB *readyQueue[MAX_QUEUE];
int rq_front = 0, rq_rear = 0;
int current_time = 0;
int context_switch_time = 1;  // 1 unit for switch

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
        int start_time = current_time;
        int end_time = start_time + p->burst_time;

        printf("| P%d (%d-%d) | ", p->pid, start_time, end_time);
        dispatchProcess(p);

        while (p->remaining_time > 0) {
            p->remaining_time--;
            p->progress = ((float)(p->burst_time - p->remaining_time) / p->burst_time) * 100;
            printf("\nProcess %d running... %.2f%% complete", p->pid, p->progress);
        }

        terminateProcess(p);
        current_time = end_time;

        // Context switch
        printf(" → Context Switch (%d-%d)\n", current_time, current_time + context_switch_time);
        current_time += context_switch_time;
    }
}
