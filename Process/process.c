#include "process.h"
#include "db_logger.h"
#include <stdio.h>

void admitProcess(PCB *p) {
    logTransition(p->pid, p->state, READY, p->remaining_time, p->progress);
    p->state = READY;
}

void dispatchProcess(PCB *p) {
    logTransition(p->pid, p->state, RUNNING, p->remaining_time, p->progress);
    p->state = RUNNING;
}

void blockProcess(PCB *p) {
    logTransition(p->pid, p->state, WAITING, p->remaining_time, p->progress);
    p->state = WAITING;
}

void suspendReady(PCB *p) {
    logTransition(p->pid, p->state, SUSP_READY, p->remaining_time, p->progress);
    p->state = SUSP_READY;
}

void suspendWaiting(PCB *p) {
    logTransition(p->pid, p->state, SUSP_WAITING, p->remaining_time, p->progress);
    p->state = SUSP_WAITING;
}

void terminateProcess(PCB *p) {
    p->progress = 100.0;
    p->remaining_time = 0;
    logTransition(p->pid, p->state, TERMINATED, p->remaining_time, p->progress);
    p->state = TERMINATED;
}
