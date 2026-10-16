#include "process.h"
#include <stdio.h>

void fcfs(Process p[], int n) {
    int time = 0;
    for (int i = 0; i < n; i++) {
        if (time < p[i].arrival_time) time = p[i].arrival_time;
        p[i].start_time = time;
        p[i].completion_time = time + p[i].burst_time;
        p[i].turnaround_time = p[i].completion_time - p[i].arrival_time;
        p[i].waiting_time = p[i].turnaround_time - p[i].burst_time;
        p[i].response_time = p[i].start_time - p[i].arrival_time;
        p[i].progress = 100.0;
        p[i].state = TERMINATED;
        time += p[i].burst_time;
    }
}
