#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_PROCESSES 100

typedef struct {
    int process_id;
    int arrival_time;
    int burst_time;
    int priority;
    int remaining_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
} Process;

typedef struct {
    int process_id;
    int start_time;
    int duration;
} ExecutionStep;

// Function prototypes
void fcfs(Process processes[], int n, ExecutionStep steps[], int *step_count);
void sjf(Process processes[], int n, ExecutionStep steps[], int *step_count);
void srtf(Process processes[], int n, ExecutionStep steps[], int *step_count);
void priority_scheduling(Process processes[], int n, ExecutionStep steps[], int *step_count);
void round_robin(Process processes[], int n, int quantum, ExecutionStep steps[], int *step_count);
void sort_by_arrival(Process processes[], int n);
void sort_by_burst_time(Process processes[], int n);
void sort_by_priority(Process processes[], int n);
void calculate_metrics(Process processes[], int n, float *avg_ct, float *avg_tat, float *avg_wt);

int main() {
    char algorithm[20];
    int quantum = 0;
    int n = 0;
    Process processes[MAX_PROCESSES];
    ExecutionStep steps[MAX_PROCESSES * 2];
    int step_count = 0;
    float avg_ct, avg_tat, avg_wt;

    // Read algorithm choice
    scanf("%19s", algorithm);
    
    // Read quantum if it's RR
    if (strcmp(algorithm, "ROBIN") == 0) {
        scanf("%d", &quantum);
    }

    // Read number of processes
    scanf("%d", &n);

    // Read process data
    for (int i = 0; i < n; i++) {
        scanf("%d %d %d %d", 
              &processes[i].process_id,
              &processes[i].arrival_time,
              &processes[i].burst_time,
              &processes[i].priority);
        processes[i].remaining_time = processes[i].burst_time;
    }

    // Execute selected algorithm
    if (strcmp(algorithm, "FCFS") == 0) {
        fcfs(processes, n, steps, &step_count);
    } else if (strcmp(algorithm, "SJF") == 0) {
        sjf(processes, n, steps, &step_count);
    } else if (strcmp(algorithm, "SRTF") == 0) {
        srtf(processes, n, steps, &step_count);
    } else if (strcmp(algorithm, "PRIORITY") == 0) {
        priority_scheduling(processes, n, steps, &step_count);
    } else if (strcmp(algorithm, "ROBIN") == 0) {
        round_robin(processes, n, quantum, steps, &step_count);
    }

    // Calculate metrics
    calculate_metrics(processes, n, &avg_ct, &avg_tat, &avg_wt);
    
    // Print metrics
    printf("Average Completion Time: %.2f\n", avg_ct);
    printf("Average Turnaround Time: %.2f\n", avg_tat);
    printf("Average Waiting Time : %.2f\n", avg_wt);
    
    // Print execution steps
    printf("\nExecution Steps:\n");
    for (int i = 0; i < step_count; i++) {
        printf("Process %d: Start Time = %d, Duration = %d\n",
               steps[i].process_id, steps[i].start_time, steps[i].duration);
    }

    return 0;
}

void calculate_metrics(Process processes[], int n, float *avg_ct, float *avg_tat, float *avg_wt) {
    float total_ct = 0, total_tat = 0, total_wt = 0;
    
    for (int i = 0; i < n; i++) {
        total_ct += processes[i].completion_time;
        total_tat += processes[i].turnaround_time;
        total_wt += processes[i].waiting_time;
    }
    
    *avg_ct = total_ct / n;
    *avg_tat = total_tat / n;
    *avg_wt = total_wt / n;
}

// First Come First Serve
void fcfs(Process processes[], int n, ExecutionStep steps[], int *step_count) {
    sort_by_arrival(processes, n);
    int current_time = 0;
    *step_count = 0;

    for (int i = 0; i < n; i++) {
        if (current_time < processes[i].arrival_time) {
            current_time = processes[i].arrival_time;
        }

        steps[*step_count].process_id = processes[i].process_id;
        steps[*step_count].start_time = current_time;
        steps[*step_count].duration = processes[i].burst_time;
        (*step_count)++;

        current_time += processes[i].burst_time;
        processes[i].completion_time = current_time;
        processes[i].turnaround_time = processes[i].completion_time - processes[i].arrival_time;
        processes[i].waiting_time = processes[i].turnaround_time - processes[i].burst_time;
    }
}

// Shortest Job First (Non-preemptive)
void sjf(Process processes[], int n, ExecutionStep steps[], int *step_count) {
    Process temp[MAX_PROCESSES];
    memcpy(temp, processes, n * sizeof(Process));
    int current_time = 0;
    int completed = 0;
    *step_count = 0;

    while (completed < n) {
        int shortest_job = -1;
        int min_burst = INT_MAX;

        for (int i = 0; i < n; i++) {
            if (temp[i].arrival_time <= current_time && temp[i].remaining_time > 0) {
                if (temp[i].burst_time < min_burst) {
                    min_burst = temp[i].burst_time;
                    shortest_job = i;
                }
            }
        }

        if (shortest_job == -1) {
            current_time++;
            continue;
        }

        steps[*step_count].process_id = temp[shortest_job].process_id;
        steps[*step_count].start_time = current_time;
        steps[*step_count].duration = temp[shortest_job].burst_time;
        (*step_count)++;

        current_time += temp[shortest_job].burst_time;
        temp[shortest_job].completion_time = current_time;
        temp[shortest_job].turnaround_time = temp[shortest_job].completion_time - temp[shortest_job].arrival_time;
        temp[shortest_job].waiting_time = temp[shortest_job].turnaround_time - temp[shortest_job].burst_time;
        temp[shortest_job].remaining_time = 0;
        completed++;
    }

    for (int i = 0; i < n; i++) {
        processes[i] = temp[i];
    }
}

// Shortest Remaining Time First (Preemptive SJF)
void srtf(Process processes[], int n, ExecutionStep steps[], int *step_count) {
    Process temp[MAX_PROCESSES];
    memcpy(temp, processes, n * sizeof(Process));
    int current_time = 0;
    int completed = 0;
    *step_count = 0;

    // Find first arrival time if no process at time 0
    if (n > 0) {
        int first_arrival = temp[0].arrival_time;
        for (int i = 1; i < n; i++) {
            if (temp[i].arrival_time < first_arrival) {
                first_arrival = temp[i].arrival_time;
            }
        }
        current_time = first_arrival;
    }

    while (completed < n) {
        int shortest_job = -1;
        int min_remaining = INT_MAX;

        // Find shortest remaining job (with FCFS tie-breaker)
        for (int i = 0; i < n; i++) {
            if (temp[i].arrival_time <= current_time && 
                temp[i].remaining_time > 0) {
                if (temp[i].remaining_time < min_remaining ||
                    (temp[i].remaining_time == min_remaining && 
                     temp[i].arrival_time < temp[shortest_job].arrival_time)) {
                    min_remaining = temp[i].remaining_time;
                    shortest_job = i;
                }
            }
        }

        if (shortest_job == -1) {
            current_time++;
            continue;
        }

        // Execute for 1 time unit
        temp[shortest_job].remaining_time--;
        current_time++;

        // Check if we can extend the last step
        if (*step_count > 0 && 
            steps[*step_count-1].process_id == temp[shortest_job].process_id &&
            steps[*step_count-1].start_time + steps[*step_count-1].duration == current_time - 1) {
            steps[*step_count-1].duration++;
        } else {
            steps[*step_count].process_id = temp[shortest_job].process_id;
            steps[*step_count].start_time = current_time - 1;
            steps[*step_count].duration = 1;
            (*step_count)++;
        }

        // Check if process completed
        if (temp[shortest_job].remaining_time == 0) {
            temp[shortest_job].completion_time = current_time;
            temp[shortest_job].turnaround_time = temp[shortest_job].completion_time - temp[shortest_job].arrival_time;
            temp[shortest_job].waiting_time = temp[shortest_job].turnaround_time - temp[shortest_job].burst_time;
            completed++;
        }
    }

    // Copy back to original array
    for (int i = 0; i < n; i++) {
        processes[i] = temp[i];
    }
}

// Priority Scheduling (Non-preemptive)
void priority_scheduling(Process processes[], int n, ExecutionStep steps[], int *step_count) {
    Process temp[MAX_PROCESSES];
    memcpy(temp, processes, n * sizeof(Process));
    int current_time = 0;
    int completed = 0;
    *step_count = 0;

    while (completed < n) {
        int highest_priority = -1;
        int min_priority = INT_MAX;

        for (int i = 0; i < n; i++) {
            if (temp[i].arrival_time <= current_time && temp[i].remaining_time > 0) {
                if (temp[i].priority < min_priority) {
                    min_priority = temp[i].priority;
                    highest_priority = i;
                }
            }
        }

        if (highest_priority == -1) {
            current_time++;
            continue;
        }

        steps[*step_count].process_id = temp[highest_priority].process_id;
        steps[*step_count].start_time = current_time;
        steps[*step_count].duration = temp[highest_priority].burst_time;
        (*step_count)++;

        current_time += temp[highest_priority].burst_time;
        temp[highest_priority].completion_time = current_time;
        temp[highest_priority].turnaround_time = current_time - temp[highest_priority].arrival_time;
        temp[highest_priority].waiting_time = temp[highest_priority].turnaround_time - temp[highest_priority].burst_time;
        temp[highest_priority].remaining_time = 0;
        completed++;
    }

    for (int i = 0; i < n; i++) {
        processes[i] = temp[i];
    }
}

// Round Robin
void round_robin(Process processes[], int n, int quantum, ExecutionStep steps[], int *step_count) {
    Process temp[MAX_PROCESSES];
    memcpy(temp, processes, n * sizeof(Process));
    int current_time = 0;
    int completed = 0;
    *step_count = 0;

    while (completed < n) {
        int flag = 0;
        for (int i = 0; i < n; i++) {
            if (temp[i].remaining_time > 0 && temp[i].arrival_time <= current_time) {
                flag = 1;
                int execution_time = (temp[i].remaining_time < quantum) ? 
                                   temp[i].remaining_time : quantum;

                steps[*step_count].process_id = temp[i].process_id;
                steps[*step_count].start_time = current_time;
                steps[*step_count].duration = execution_time;
                (*step_count)++;

                temp[i].remaining_time -= execution_time;
                current_time += execution_time;

                if (temp[i].remaining_time == 0) {
                    temp[i].completion_time = current_time;
                    temp[i].turnaround_time = temp[i].completion_time - temp[i].arrival_time;
                    temp[i].waiting_time = temp[i].turnaround_time - temp[i].burst_time;
                    completed++;
                }
            }
        }
        if (!flag) current_time++;
    }

    for (int i = 0; i < n; i++) {
        processes[i] = temp[i];
    }
}

// Utility functions
void sort_by_arrival(Process processes[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (processes[j].arrival_time > processes[j + 1].arrival_time) {
                Process temp = processes[j];
                processes[j] = processes[j + 1];
                processes[j + 1] = temp;
            }
        }
    }
}

void sort_by_burst_time(Process processes[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (processes[j].burst_time > processes[j + 1].burst_time) {
                Process temp = processes[j];
                processes[j] = processes[j + 1];
                processes[j + 1] = temp;
            }
        }
    }
}

void sort_by_priority(Process processes[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (processes[j].priority > processes[j + 1].priority) {
                Process temp = processes[j];
                processes[j] = processes[j + 1];
                processes[j + 1] = temp;
            }
        }
    }
}