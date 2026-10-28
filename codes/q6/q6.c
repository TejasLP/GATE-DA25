#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/**
 * @brief Performs back-substitution to solve an upper triangular system Ux = b.
 * 
 * @param n     Size of the matrix/vector (n x n system)
 * @param U     Pointer to the 2D upper triangular matrix (coefficients)
 * @param b     Pointer to the right-hand side constant vector
 * @param x     Pointer to the solution vector where results will be stored
 */
void back_substitution(int n, double **U, double *b, double *x) {
    // Loop backwards from the last row (n-1) down to the first row (0)
    for (int i = n - 1; i >= 0; i--) {
        double sum = 0.0;
        
        // Sum up the known values of previously computed x[j] 
        // multiplied by the corresponding upper-triangle coefficient U[i][j]
        for (int j = i + 1; j < n; j++) {
            sum += U[i][j] * x[j];
        }
        
        // Isolate x[i] by subtracting the sum from b[i] and dividing by the diagonal element U[i][i]
        x[i] = (b[i] - sum) / U[i][i];
    }
}

int main() {
    // Seed the random number generator using the system clock so values change each run
    srand((unsigned int)time(NULL));

    // Open a data file to export execution times for subsequent Python plotting
    FILE *fp = fopen("timing_results.dat", "w");
    if (fp == NULL) {
        printf("Error opening file for writing!\n");
        return 1;
    }

    // Write the column headers for the data file
    fprintf(fp, "n time_ms\n");

    // Define the different matrix sizes (n) to benchmark, including smaller, mid, and larger values
    int test_sizes[] = {10, 50, 100, 250, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000};
    int num_tests = sizeof(test_sizes) / sizeof(test_sizes[0]);

    printf("=========================================================\n");
    printf(" Running Benchmarking & Exporting to 'timing_results.dat' \n");
    printf("=========================================================\n");

    // Outer loop: iterate through every test matrix size specified in test_sizes
    for (int t = 0; t < num_tests; t++) {
        int n = test_sizes[t];

        // --- 1. DYNAMIC MEMORY ALLOCATION ---
        // Allocate memory for the 2D matrix U (n rows of pointers)
        double **U = (double **)malloc(n * sizeof(double *));
        // Allocate memory for vectors b and x (size n)
        double *b = (double *)malloc(n * sizeof(double));
        double *x = (double *)malloc(n * sizeof(double));

        // Allocate memory for each individual row of matrix U
        for (int i = 0; i < n; i++) {
            U[i] = (double *)malloc(n * sizeof(double));
        }

        // --- 2. MATRIX & VECTOR INITIALIZATION ---
        // Fill b and U with random values formatted as an upper triangular system
        for (int i = 0; i < n; i++) {
            b[i] = (double)(rand() % 100 + 1); // Random right-hand side value between 1 and 100
            
            for (int j = 0; j < n; j++) {
                if (j < i) {
                    U[i][j] = 0.0;             // Lower triangle: set to 0.0 (strictly upper triangular)
                } else if (j == i) {
                    U[i][j] = (double)(rand() % 10 + 1); // Diagonal: non-zero values to prevent division by zero
                } else {
                    U[i][j] = (double)(rand() % 10);     // Upper triangle: random coefficients
                }
            }
        }

        // --- 3. ITERATION CONTROL FOR ACCURACY ---
        // Small matrices execute in microseconds, which is too fast for standard clocks to measure accurately.
        // We run multiple iterations for small sizes and average out the time.
        int iterations = (n < 100) ? 10000 : ((n < 1000) ? 100 : 1);

        // --- 4. HIGH-RESOLUTION TIMING ---
        struct timespec start, end;
        clock_gettime(CLOCK_MONOTONIC, &start); // Mark the start timestamp

        // Run back-substitution 'iterations' times
        for (int iter = 0; iter < iterations; iter++) {
            back_substitution(n, U, b, x);
        }

        clock_gettime(CLOCK_MONOTONIC, &end); // Mark the end timestamp

        // --- 5. TIME CALCULATION ---
        // Convert difference in seconds and nanoseconds into total milliseconds.
        // We divide by 'iterations' here because small matrix sizes run multiple times 
        // back-to-back to accumulate enough measurable duration, and dividing scales 
        // the total cumulative duration back down to find the average time for a single execution.
        double elapsed_ms = ((end.tv_sec - start.tv_sec) * 1000.0 + 
                             (end.tv_nsec - start.tv_nsec) / 1000000.0) / iterations;

        // --- 6. EXPORTING AND LOGGING ---
        // Save the matrix size and its measured execution time to the .dat file
        fprintf(fp, "%d %.6f\n", n, elapsed_ms);
        // Print a clean status report to the terminal console
        printf("n = %-5d | Time = %.6f ms\n", n, elapsed_ms);

        // --- 7. CLEANUP / MEMORY DEALLOCATION ---
        // Free all dynamically allocated memory to prevent memory leaks
        for (int i = 0; i < n; i++) {
            free(U[i]);
        }
        free(U);
        free(b);
        free(x);
    }

    // Close the data file handler
    fclose(fp);
    printf("=========================================================\n");
    printf("Done! Data saved to 'timing_results.dat'.\n");

    return 0;
}
