#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define MAX_RESOURCES 10
#define MAX_PROCESSES 10

typedef struct {
    char processName[20];
    int allocation[MAX_RESOURCES];
    int max[MAX_RESOURCES];
    int need[MAX_RESOURCES];
    int priority;
} ResourceAllocation;

int available[MAX_RESOURCES];
ResourceAllocation processes[MAX_PROCESSES];
int processCount = 0;
int resourceCount = 0;

void calculateNeed(ResourceAllocation *process, int resourceCount) {
    for (int i = 0; i < resourceCount; i++) {
        process->need[i] = process->max[i] - process->allocation[i];
    }
}

void addProcess(const char *processName, int *allocation, int *max, int priority) {
    if (processCount >= MAX_PROCESSES) {
        printf("Cannot add more processes. Limit reached.\n");
        return;
    }

    ResourceAllocation *process = &processes[processCount];
    strcpy(process->processName, processName);
    memcpy(process->allocation, allocation, sizeof(int) * resourceCount);
    memcpy(process->max, max, sizeof(int) * resourceCount);
    process->priority = priority;

    calculateNeed(process, resourceCount);

    processCount++;
    printf("Process %s added successfully.\n", processName);
}

void runBankersAlgorithm() {
    int work[MAX_RESOURCES];
    bool finish[MAX_PROCESSES] = {false};
    char safeSequence[MAX_PROCESSES][20];
    int safeSequenceCount = 0;

    memcpy(work, available, sizeof(int) * resourceCount);

    bool progress = true;
    while (progress) {
        progress = false;
        for (int i = 0; i < processCount; i++) {
            if (!finish[i]) {
                bool canProceed = true;
                for (int j = 0; j < resourceCount; j++) {
                    if (processes[i].need[j] > work[j]) {
                        canProceed = false;
                        break;
                    }
                }
                if (canProceed) {
                    for (int j = 0; j < resourceCount; j++) {
                        work[j] += processes[i].allocation[j];
                    }
                    finish[i] = true;
                    strcpy(safeSequence[safeSequenceCount++], processes[i].processName);
                    progress = true;
                }
            }
        }
    }

    bool allFinished = true;
    for (int i = 0; i < processCount; i++) {
        if (!finish[i]) {
            allFinished = false;
            break;
        }
    }

    if (allFinished) {
        printf("\nSYSTEM IS IN SAFE STATE!.\nSAFE SEQUENCE : ");
        for (int i = 0; i < safeSequenceCount; i++) {
            printf("%s%s", safeSequence[i], i == safeSequenceCount - 1 ? "\n" : " -> ");
        }
    } else {
        printf("\nSYSTEM IS IN DEADLOCK STATE!\n");
    }
}

int main() {
    // Detect available resource count
    char line[256];
    if (!fgets(line, sizeof(line), stdin)) {
        fprintf(stderr, "Error reading available resources.\n");
        return 1;
    }

    // Parse the line and count resource types
    char *token = strtok(line, " \t\n");
    while (token && resourceCount < MAX_RESOURCES) {
        available[resourceCount++] = atoi(token);
        token = strtok(NULL, " \t\n");
    }

    // Read the processes
    while (fgets(line, sizeof(line), stdin)) {
        if (strncmp(line, "END", 3) == 0) break;

        char name[20];
        int alloc[MAX_RESOURCES], maxd[MAX_RESOURCES];

        token = strtok(line, " \t\n");
        if (!token) continue;
        strcpy(name, token);

        for (int i = 0; i < resourceCount; i++) {
            token = strtok(NULL, " \t\n");
            if (!token) {
                fprintf(stderr, "Error: Not enough allocation values for %s\n", name);
                return 1;
            }
            alloc[i] = atoi(token);
        }

        for (int i = 0; i < resourceCount; i++) {
            token = strtok(NULL, " \t\n");
            if (!token) {
                fprintf(stderr, "Error: Not enough max values for %s\n", name);
                return 1;
            }
            maxd[i] = atoi(token);
        }

        addProcess(name, alloc, maxd, 0);
    }

    // Run the Banker's Algorithm
    runBankersAlgorithm();

    return 0;
}
