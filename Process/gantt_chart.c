#include "process.h"
#include <stdio.h>

void printGanttChart(PCB processes[], int n) {
    printf("\nGantt Chart:\n");
    for (int i = 0; i < n; i++) {
        printf("| P%d ", processes[i].pid);
    }
    printf("|\n");
}
