#include "process.h"
#include <stdio.h>

void roundRobin(Process p[], int n, int quantum) {
    int time = 0, completed = 0;
    while (completed < n) {
        for (int i = 0; i < n; i++) {
            if (p[i].remaining_time > 0 && p[i].arrival_time <= time) {
                p[i].state = RUNNING;
                int exec_time = (p[i].remaining_time > quantum) ? quantum : p[i].remaining_time;

                if (p[i].burst_time == p[i].remaining_time)
                    p[i].start_time = time;

                for (int t = 1; t <= exec_time; t++) {
                    time++;
                    p[i].remaining_time--;
                    p[i].progress = ((float)(p[i].burst_time - p[i].remaining_time) / p[i].burst_time) * 100.0;
                    printf("Time %d | Process %d (%s) RUNNING | %.2f%% complete\n",
                           time, p[i].pid, p[i].name, p[i].progress);
                }

                if (p[i].remaining_time == 0) {
                    p[i].completion_time = time;
                    p[i].turnaround_time = p[i].completion_time - p[i].arrival_time;
                    p[i].waiting_time = p[i].turnaround_time - p[i].burst_time;
                    p[i].response_time = p[i].start_time - p[i].arrival_time;
                    p[i].state = TERMINATED;
                    completed++;
                    printf("Process %d (%s) TERMINATED at %d\n", p[i].pid, p[i].name, time);
                } else {
                    p[i].state = WAITING;
                    printf("Context Switch → Process %d (%s) WAITING at %d\n", p[i].pid, p[i].name, time);
                }
            }
        }
    }
}
