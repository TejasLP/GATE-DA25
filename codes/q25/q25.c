#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define NUM_SAMPLES 100000 // Large sample size N = 100,000
#define PLOT_STEP   100    // Export every 100th sorted point (1,000 points) to keep PDF vector size fast

// Comparator function for qsort (ascending order)
int compare_doubles(const void *a, const void *b) {
    double diff = (*(const double *)a) - (*(const double *)b);
    return (diff > 0) - (diff < 0);
}

int main(void) {
    srand(42); // Fixed seed for reproducibility

    double *X = (double *)malloc(NUM_SAMPLES * sizeof(double));
    if (X == NULL) {
        perror("Memory allocation failed");
        return EXIT_FAILURE;
    }

    int count_in_interval = 0;

    // 1. Generate U ~ Uniform(0, 1) and compute X = 2*sqrt(U) - 1
    for (int i = 0; i < NUM_SAMPLES; i++) {
        double U = (double)rand() / (double)RAND_MAX;
        X[i] = 2.0 * sqrt(U) - 1.0;

        if (X[i] * X[i] <= 0.25) {
            count_in_interval++;
        }
    }

    // 2. Sort X in ascending order to construct the Empirical CDF via index
    qsort(X, NUM_SAMPLES, sizeof(double), compare_doubles);

    // 3. Export sorted X and normalized index (i + 1)/N to simulated_cdf.dat
    FILE *fp = fopen("simulated_cdf.dat", "w");
    if (fp == NULL) {
        perror("Error opening file");
        free(X);
        return EXIT_FAILURE;
    }

    fprintf(fp, "# x_sorted\tsimulated_cdf_index\n");
    for (int i = 0; i < NUM_SAMPLES; i += PLOT_STEP) {
        double empirical_cdf = (double)(i + 1) / (double)NUM_SAMPLES;
        fprintf(fp, "%.6f\t%.6f\n", X[i], empirical_cdf);
    }
    // Always include the final sample point at index N - 1
    fprintf(fp, "%.6f\t%.6f\n", X[NUM_SAMPLES - 1], 1.0);

    fclose(fp);

    // 4. Print verification results
    double sim_prob = (double)count_in_interval / (double)NUM_SAMPLES;
    printf("=== GATE DA 2025 Q1.2.25: Inverse Transform Sampling Verification ===\n");
    printf("Inverse CDF Relation : X = 2*sqrt(U) - 1, where U ~ Uniform(0, 1)\n");
    printf("Sample Size (N)      : %d\n", NUM_SAMPLES);
    printf("Theoretical P(X^2 <= 0.25) : 0.500000\n");
    printf("Simulated   P(X^2 <= 0.25) : %.6f\n", sim_prob);
    printf("Exported sorted empirical CDF data to simulated_cdf.dat\n");

    free(X);
    return EXIT_SUCCESS;
}
