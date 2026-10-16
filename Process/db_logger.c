#include <stdio.h>
#include "process.h"

void logProcessResult(Process *p) {
    FILE *fp = fopen("process_results.csv", "a");
    if (!fp) return;
    fprintf(fp, "%d,%s,%d,%d,%d,%d,%s\n",
            p->pid, p->name, p->burst_time,
            p->completion_time, p->turnaround_time,
            p->waiting_time, p->algorithm_used);
    fclose(fp);
}
