#ifndef PROCESS_H
#define PROCESS_H

typedef enum 
{
    NEW, READY, RUNNING, WAITING, SUSP_READY, SUSP_WAITING, TERMINATED
} State;

typedef struct 
{
    int pid;
    State state;
    int priority;
    int burst_time;
    int remaining_time;
    int arrival_time;
    int completion_time;
    float progress;   // % completed
} PCB;


void admitProcess(PCB *p);
void dispatchProcess(PCB *p);
void blockProcess(PCB *p);
void suspendReady(PCB *p);
void suspendWaiting(PCB *p);
void terminateProcess(PCB *p);

#endif
