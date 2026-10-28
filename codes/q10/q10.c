#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define N 1000000  // Number of Monte Carlo samples
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// Function to generate a standard normal variable Z ~ N(0,1)
// from standard uniform variables U1, U2 ~ Uniform(0,1) using Box-Muller transform
double generate_standard_normal() {
    double u1 = (double)rand() / ((double)RAND_MAX + 1.0);
    double u2 = (double)rand() / ((double)RAND_MAX + 1.0);
    
    // Prevent log(0)
    while (u1 <= 1e-15) {
        u1 = (double)rand() / ((double)RAND_MAX + 1.0);
    }
    
    return sqrt(-2.0 * log(u1)) * cos(2.0 * M_PI * u2);
}

typedef struct {
    double a;
    double b;
    const char* label;
} Option;

int main() {
    srand(42); // Fixed seed for reproducibility

    // Define the 4 options from the problem
    Option options[4] = {
        {-2.0,  1.0, "i)  a = -2, b = 1"},
        { 2.0, -1.0, "ii) a = 2,  b = -1"},
        {-2.0, -1.0, "iii) a = -2, b = -1"},
        { 1.0,  1.0, "iv) a = 1,  b = 1"}
    };

    printf("========================================================================================\n");
    printf("%-20s | E[X] (Target: 1.0) | E[(X-E[X])Z] (Target: -2.0) | E[(X-E[X])^2] (Target: 4.0)\n", "Option");
    printf("========================================================================================\n");

    for (int k = 0; k < 4; k++) {
        double a = options[k].a;
        double b = options[k].b;

        double sum_X = 0.0;
        double sum_cov = 0.0;
        double sum_var = 0.0;

        // Arrays to store Z and X to compute expectations cleanly
        double *Z = (double *)malloc(N * sizeof(double));
        double *X = (double *)malloc(N * sizeof(double));

        for (int i = 0; i < N; i++) {
            Z[i] = generate_standard_normal();
            X[i] = a * Z[i] + b;
            sum_X += X[i];
        }

        double mean_X = sum_X / N;

        for (int i = 0; i < N; i++) {
            double diff = X[i] - mean_X;
            sum_cov += diff * Z[i];
            sum_var += diff * diff;
        }

        double exp_cov = sum_cov / N;
        double exp_var = sum_var / N;

        printf("%-20s | %18.4f | %25.4f | %25.4f\n", 
               options[k].label, mean_X, exp_cov, exp_var);

        free(Z);
        free(X);
    }

    printf("========================================================================================\n");

    return 0;
}
