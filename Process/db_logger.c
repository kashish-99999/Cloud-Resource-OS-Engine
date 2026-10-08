#include "db_logger.h"
#include <stdio.h>

void logTransition(int pid, State oldState, State newState, int remaining, float progress) {
    printf("[DB LOG] PID=%d: %d -> %d | Remaining=%d | Progress=%0.2f%%\n",
           pid, oldState, newState, remaining, progress);
}
