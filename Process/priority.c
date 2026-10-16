#include "process.h"
#include <stdio.h>

void priority_np(Process p[], int n) {
    int time = 0, completed = 0;
    while (completed < n) {
        int idx = -1, best_prio = 9999;
        for (int i = 0; i < n; i++) {
            if (p[i].arrival_time <= time && p[i].state != TERMINATED && p[i].priority < best_prio) {
                best_prio = p[i].priority;
                idx = i;
            }
        }
        if (idx == -1) { time++; continue; }
        p[idx].start_time = time;
        time += p[idx].burst_time;
        p[idx].completion_time = time;
        p[idx].turnaround_time = p[idx].completion_time - p[idx].arrival_time;
        p[idx].waiting_time = p[idx].turnaround_time - p[idx].burst_time;
        p[idx].response_time = p[idx].start_time - p[idx].arrival_time;
        p[idx].progress = 100.0;
        p[idx].state = TERMINATED;
        completed++;
    }
}
