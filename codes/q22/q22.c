#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define NUM_SAMPLES 10000000 // 10 million samples for high Monte Carlo accuracy

// Generate a normal random variable X ~ N(mu, sigma^2) using the Box-Muller transform
double generate_normal(double mu, double sigma) {
    static int has_spare = 0;
    static double spare;

    if (has_spare) {
        has_spare = 0;
        return mu + sigma * spare;
    }

    has_spare = 1;
    double u1, u2;
    do {
        u1 = (double)rand() / RAND_MAX;
    } while (u1 <= 1e-15); // Avoid log(0)
    u2 = (double)rand() / RAND_MAX;

    double mag = sqrt(-2.0 * log(u1));
    double z0  = mag * cos(2.0 * M_PI * u2);
    spare      = mag * sin(2.0 * M_PI * u2);

    return mu + sigma * z0;
}

int main(void) {
    srand(42); // Fixed seed for reproducible verification

    // Arbitrary parameters for X ~ N(mu, sigma^2)
    const double mu = 5.0;
    const double sigma = 3.0;

    double sum_Y = 0.0;    // Accumulates Y = Z^2 to compute E[Z^2]
    double sum_Y2 = 0.0;   // Accumulates Y^2 = Z^4 to compute E[Z^4]

    for (long i = 0; i < NUM_SAMPLES; i++) {
        // 1. Generate X ~ N(mu, sigma^2)
        double X = generate_normal(mu, sigma);

        // 2. Standardize: Z = (X - mu) / sigma
        double Z = (X - mu) / sigma;

        // 3. Transform: Y = Z^2
        double Y = Z * Z;

        sum_Y  += Y;
        sum_Y2 += Y * Y;
    }

    // Empirical expectations and variance
    double E_Y   = sum_Y / NUM_SAMPLES;          // E[Y] = E[Z^2]
    double E_Y2  = sum_Y2 / NUM_SAMPLES;         // E[Y^2] = E[Z^4]
    double var_Y = E_Y2 - (E_Y * E_Y);           // Var(Y) = E[Z^4] - (E[Z^2])^2

    // Theoretical values
    const double theo_E_Z2  = 1.0;
    const double theo_E_Z4  = 3.0;
    const double theo_var_Y = 2.0;

    printf("=== GATE DA 2025 Q1.2.22: Monte Carlo Verification of Var(Y) ===\n");
    printf("Parameters: X ~ N(mu = %.1f, sigma^2 = %.1f), Samples = %d\n\n",
           mu, sigma * sigma, NUM_SAMPLES);

    printf("%-18s | %-15s | %-15s | %-12s\n", "Quantity", "Theoretical", "Empirical (C)", "Abs Error");
    printf("----------------------------------------------------------------------\n");
    printf("%-18s | %15.6f | %15.6f | %12.6f\n",
           "E[Y] = E[Z^2]", theo_E_Z2, E_Y, fabs(E_Y - theo_E_Z2));
    printf("%-18s | %15.6f | %15.6f | %12.6f\n",
           "E[Y^2] = E[Z^4]", theo_E_Z4, E_Y2, fabs(E_Y2 - theo_E_Z4));
    printf("%-18s | %15.6f | %15.6f | %12.6f\n",
           "Var(Y)", theo_var_Y, var_Y, fabs(var_Y - theo_var_Y));

    printf("\nVerified Result: Var(Y) = %.2f -> Matches Option (ii) 2\n", round(var_Y));

    return EXIT_SUCCESS;
}
