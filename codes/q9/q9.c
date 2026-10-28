#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int n = 500; // Large sample size for smooth empirical convergence
    FILE *fp = fopen("uniform_samples.dat", "w");
    if (fp == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    // Seed random number generator
    srand(time(NULL));

    for (int i = 0; i < n; i++) {
        // Generate U uniformly distributed on [0, 1]
        double U = (double)rand() / (double)RAND_MAX;
        // Transform to X = 2U + 2
        double X = 2.0 * U + 2.0;
        
        // Write U and X to the .dat file
        fprintf(fp, "%lf %lf\n", U, X);
    }

    fclose(fp);
    printf("Successfully generated %d uniform samples in uniform_samples.dat\n", n);
    return 0;
}
