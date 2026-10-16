#ifndef PROCESS_H
#define PROCESS_H

#include <time.h>

typedef enum {
    NEW, READY, RUNNING, WAITING,
    SUSP_READY, SUSP_WAITING, TERMINATED
} State;

typedef struct {
    int pid;
    char name[10];
    int arrival_time;
    int burst_time;
    int remaining_time;
    int priority;
    int completion_time;
    int turnaround_time;
    int waiting_time;
    int start_time;
    int response_time;
    float progress;
    int completion_percent;
    State state;
    time_t enter_time;
    time_t leave_time;
    char algorithm_used[20];
} Process;

char* getTimeStr();
void displayPCB(Process *p);
void changeState(Process *p, State new_state);

#endif
