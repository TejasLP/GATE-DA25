#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define N 5000000      // Total number of samples for high accuracy
#define NUM_BINS 1000   // Number of discrete bins used to handle continuous conditioning on Y

int main() {
    srand((unsigned int)time(NULL));

    // Variable to accumulate all X values for calculating the overall expected value E[X]
    double total_X = 0.0;

    // --- DYNAMIC ALLOCATION FOR SIMULATION ---
    // sum_X_given_Y: Stores the running sum of X values for each Y-bin
    double *sum_X_given_Y = (double *)calloc(NUM_BINS, sizeof(double));
    
    // count_Y: Stores how many samples fall into each Y-bin
    int *count_Y = (int *)calloc(NUM_BINS, sizeof(int));
    
    // Arrays to store generated sample values for X and Y
    double *samples_X = (double *)malloc(N * sizeof(double));
    double *samples_Y = (double *)malloc(N * sizeof(double));

    // Check if memory allocation was successful
    if (!sum_X_given_Y || !count_Y || !samples_X || !samples_Y) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    // Define the range of Y. Since Y = X + noise, and X in [0,1], 
    // Y will roughly range from -0.5 to 1.5.
    double y_min = -0.5;
    double y_max = 1.5;
    double bin_width = (y_max - y_min) / NUM_BINS; // Width of each individual bin

    // =========================================================================
    // STEP 1: Generate samples and populate tracking bins
    // =========================================================================
    for (int i = 0; i < N; i++) {
        // Generate X as a continuous Uniform(0, 1) random variable
        // (double)rand() / RAND_MAX maps random integers to a float between 0.0 and 1.0
        samples_X[i] = (double)rand() / (double)RAND_MAX;
        
        // Generate Y dependent on X by adding uniform noise from [-0.5, 0.5]
        double noise = ((double)rand() / (double)RAND_MAX) - 0.5;
        samples_Y[i] = samples_X[i] + noise;

        // Accumulate X to calculate global E[X] later
        total_X += samples_X[i];

        // Since Y is continuous, the probability of Y equaling any exact decimal is zero.
        // We map Y into a discrete bin index to approximate E[X | Y = y].
        int bin_idx = (int)((samples_Y[i] - y_min) / bin_width);

        // Ensure the bin index is within safe array bounds
        if (bin_idx >= 0 && bin_idx < NUM_BINS) {
            sum_X_given_Y[bin_idx] += samples_X[i]; // Add X value to this bin's running sum
            count_Y[bin_idx]++;                      // Increment sample count for this bin
        }
    }

    // Calculate the overall expected value E[X] (Theoretical value for Uniform(0,1) is 0.5)
    double E_X = total_X / N;

    // =========================================================================
    // STEP 2: Compute conditional expectations E[X | Y = y] for each bin
    // =========================================================================
    double E_X_given_Y_bin[NUM_BINS];
    for (int b = 0; b < NUM_BINS; b++) {
        if (count_Y[b] > 0) {
            // Conditional mean for bin b = (Sum of X in bin b) / (Total count in bin b)
            E_X_given_Y_bin[b] = sum_X_given_Y[b] / count_Y[b];
        } else {
            E_X_given_Y_bin[b] = 0.0; // Avoid division by zero for empty bins
        }
    }

    // =========================================================================
    // STEP 3: Compute the outer expectation E[E[X | Y]]
    // =========================================================================
    // To find E[E[X | Y]], we substitute each sample's Y value with the conditional 
    // expectation of its respective bin, and then take the average across all samples.
    double total_conditional_expectation = 0.0;
    int valid_samples = 0;

    for (int i = 0; i < N; i++) {
        // Find which bin this sample's Y belongs to
        int bin_idx = (int)((samples_Y[i] - y_min) / bin_width);
        
        if (bin_idx >= 0 && bin_idx < NUM_BINS && count_Y[bin_idx] > 0) {
            // Add the conditional expectation value linked to this Y
            total_conditional_expectation += E_X_given_Y_bin[bin_idx];
            valid_samples++;
        }
    }

    // Final outer expectation average
    double E_E_X_given_Y = total_conditional_expectation / valid_samples;

    // =========================================================================
    // STEP 4: Output and verify results
    // =========================================================================
    printf("=====================================================\n");
    printf(" Verification: E[E[X|Y]] = E[X] for X ~ Uniform(0,1) \n");
    printf("=====================================================\n");
    printf("Number of Samples (N) : %d\n", N);
    printf("Theoretical E[X]      : 0.500000\n");
    printf("Simulated E[X]        : %.6f\n", E_X);
    printf("Simulated E[E[X | Y]] : %.6f\n", E_E_X_given_Y);
    printf("Absolute Difference   : %.6f\n", fabs(E_X - E_E_X_given_Y));
    printf("=====================================================\n");

    // Free all dynamically allocated memory to prevent memory leaks
    free(sum_X_given_Y);
    free(count_Y);
    free(samples_X);
    free(samples_Y);

    return 0;
}
