#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "process.h"

char* getTimeStr() {
    static char buffer[30];
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    strftime(buffer, sizeof(buffer), "%H:%M:%S", t);
    return buffer;
}

void displayPCB(Process *p) {
    const char *state_names[] = {
        "NEW","READY","RUNNING","WAITING",
        "SUSP_READY","SUSP_WAITING","TERMINATED"
    };
    printf("📄 PCB Info → PID=%d | Name=%s | State=%s | Burst=%d | Remaining=%d | Priority=%d | Completion=%d%%\n",
           p->pid, p->name, state_names[p->state],
           p->burst_time, p->remaining_time,
           p->priority, p->completion_percent);
}

void changeState(Process *p, State new_state) {
    const char *state_names[] = {
        "NEW","READY","RUNNING","WAITING",
        "SUSP_READY","SUSP_WAITING","TERMINATED"
    };

    p->leave_time = time(NULL);
    printf("\n🕒 [%s] Process %s leaving %s\n",
           getTimeStr(), p->name, state_names[p->state]);

    p->enter_time = time(NULL);
    p->state = new_state;
    printf("🕒 [%s] Process %s entering %s\n",
           getTimeStr(), p->name, state_names[new_state]);

    if (new_state == RUNNING) {
        p->completion_percent += rand() % 30;
        if (p->completion_percent > 100) p->completion_percent = 100;
        p->remaining_time -= rand() % 3;
        if (p->remaining_time < 0) p->remaining_time = 0;
    }

    displayPCB(p);
}
