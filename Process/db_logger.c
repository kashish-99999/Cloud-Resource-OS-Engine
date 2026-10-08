#include <stdio.h>
#include <stdlib.h>
#include <libpq-fe.h>
#include "db_logger.h"

// Function to log a process transition into PostgreSQL
void logTransition(int pid, State oldState, State newState, int remaining, float progress) {
    // Connect to PostgreSQL
    PGconn *conn = PQconnectdb("host=localhost dbname=cloud_resource_os user=postgres password=kashish");

    if (PQstatus(conn) != CONNECTION_OK) {
        fprintf(stderr, "Connection failed: %s\n", PQerrorMessage(conn));
        PQfinish(conn);
        return;
    }

    // Build SQL query
    char query[512];
    snprintf(query, sizeof(query),
        "INSERT INTO process_log (pid, old_state, new_state, remaining_time, progress) "
        "VALUES (%d, '%d', '%d', %d, %.2f);",
        pid, oldState, newState, remaining, progress);

    // Execute query
    PGresult *res = PQexec(conn, query);
    if (PQresultStatus(res) != PGRES_COMMAND_OK) {
        fprintf(stderr, "Insert failed: %s\n", PQerrorMessage(conn));
    }

    // Cleanup
    PQclear(res);
    PQfinish(conn);
}
