#include "process.h"
#include "scheduler.h"
#include "gantt_chart.h"

int main() {
    PCB p1 = {1, NEW, 1, 5, 5, 0, 0, 0.0};
    PCB p2 = {2, NEW, 2, 3, 3, 0, 0, 0.0};

    admitProcess(&p1);
    admitProcess(&p2);

    enqueueReady(&p1);
    enqueueReady(&p2);

    runScheduler();

    PCB processes[] = {p1, p2};
    printGanttChart(processes, 2);

    return 0;
}
