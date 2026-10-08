#ifndef DB_LOGGER_H
#define DB_LOGGER_H

#include "process.h"

void logTransition(int pid, State oldState, State newState, int remaining, float progress);

#endif
