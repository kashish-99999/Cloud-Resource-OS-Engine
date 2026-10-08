#include "process.h"
#include <stdio.h>

void printGanttChart(PCB processes[], int n) {
    printf("\nGantt Chart:\n");
    int time = 0;
    for (int i = 0; i < n; i++) {
        printf("| P%d (%d-%d) | ", processes[i].pid, time, time + processes[i].burst_time);
        time += processes[i].burst_time;
        if (i < n - 1) {
            printf("-> Context Switch (%d-%d) ", time, time + 1);
            time += 1;
        }
    }
    printf("\n");
}
