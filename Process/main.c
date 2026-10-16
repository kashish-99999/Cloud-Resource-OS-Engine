#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "process.h"
#include "scheduler.h"
#include "db_logger.h"

int main() {
    int n, choice, quantum;
    printf("Enter number of processes: ");
    scanf("%d", &n);

    Process processes[n];
    for (int i = 0; i < n; i++) {
        processes[i].pid = i + 1;
        sprintf(processes[i].name, "P%d", i + 1);
        printf("Enter arrival time, burst time, and priority for %s: ", processes[i].name);
        scanf("%d %d %d", &processes[i].arrival_time, &processes[i].burst_time, &processes[i].priority);
        processes[i].remaining_time = processes[i].burst_time;
        processes[i].completion_percent = 0;
    }

    printf("\nSelect Scheduling Algorithm:\n");
    printf("1. FCFS\n2. SJF\n3. SRTF\n4. Priority\n5. Round Robin\nChoice: ");
    scanf("%d", &choice);

    AlgoType algo;
    switch (choice) {
        case 1: algo = ALG_FCFS; strcpy(processes[0].algorithm_used, "FCFS"); break;
        case 2: algo = ALG_SJF; strcpy(processes[0].algorithm_used, "SJF"); break;
        case 3: algo = ALG_SRTF; strcpy(processes[0].algorithm_used, "SRTF"); break;
        case 4: algo = ALG_PRIORITY; strcpy(processes[0].algorithm_used, "Priority"); break;
        case 5: algo = ALG_ROUND_ROBIN; strcpy(processes[0].algorithm_used, "Round Robin");
                printf("Enter quantum: "); scanf("%d", &quantum); break;
        default: printf("Invalid choice.\n"); return 0;
    }

    runScheduler(algo, processes, n, quantum);

    printf("\n📊 Final Results:\n");
    printf("PID\tBurst\tCT\tTAT\tWT\tAlgorithm\n");
    for (int i = 0; i < n; i++) {
        processes[i].turnaround_time = processes[i].completion_time - processes[i].arrival_time;
        processes[i].waiting_time = processes[i].turnaround_time - processes[i].burst_time;
        printf("%d\t%d\t%d\t%d\t%d\t%s\n",
               processes[i].pid, processes[i].burst_time,
               processes[i].completion_time, processes[i].turnaround_time,
               processes[i].waiting_time, processes[i].algorithm_used);
        logProcessResult(&processes[i]);
    }

    printf("\n✅ Simulation completed and results saved.\n");
    return 0;
}
