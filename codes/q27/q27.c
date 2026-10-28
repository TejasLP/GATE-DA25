#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define NUM_SAMPLES 10000000 // 10 million Monte Carlo samples
#define MAX_L       6        // Track P(Y = l) for l = 0, 1, ..., 5

int main(void) {
    srand(42); // Fixed seed for reproducibility

    // Mean = 1 / ln(10) => rate parameter lambda = ln(10)
    const double lambda = log(10.0);
    const double q_theo = exp(-lambda); // e^(-ln 10) = 0.1

    long counts[MAX_L] = {0};

    for (long i = 0; i < NUM_SAMPLES; i++) {
        // Generate U ~ Uniform(0, 1], avoiding log(0)
        double u;
        do {
            u = (double)rand() / (double)RAND_MAX;
        } while (u <= 1e-15);

        // Inverse transform sampling: X ~ Exp(lambda)
        double X = -log(u) / lambda;

        // Apply floor function: Y = floor(X)
        int Y = (int)floor(X);

        if (Y >= 0 && Y < MAX_L) {
            counts[Y]++;
        }
    }

    // Empirical probabilities P(Y = l)
    double prob_emp[MAX_L];
    for (int l = 0; l < MAX_L; l++) {
        prob_emp[l] = (double)counts[l] / (double)NUM_SAMPLES;
    }

    // Estimate q from P(Y = 0) = 1 - q  =>  q = 1 - P(Y = 0)
    double q_from_l0 = 1.0 - prob_emp[0];

    // Estimate q from ratio P(Y = 1) / P(Y = 0) = [q(1 - q)] / (1 - q) = q
    double q_from_ratio = prob_emp[1] / prob_emp[0];

    printf("=== GATE DA 2025 Q1.2.27: Verification of Y = floor(X) ===\n");
    printf("Rate parameter (lambda) : ln(10) = %.6f\n", lambda);
    printf("Theoretical q = e^(-ln 10) : %.6f\n", q_theo);
    printf("Empirical q (1 - P(Y=0))   : %.6f\n", q_from_l0);
    printf("Empirical q (P(Y=1)/P(Y=0)): %.6f\n\n", q_from_ratio);

    printf("%-4s | %-18s | %-18s | %-12s\n",
           "l", "Theoretical q^l(1-q)", "Empirical P(Y=l)", "Abs Error");
    printf("----------------------------------------------------------------\n");

    for (int l = 0; l < 5; l++) {
        double prob_theo = pow(q_theo, l) * (1.0 - q_theo);
        printf("%-4d | %18.6f | %18.6f | %12.6f\n",
               l, prob_theo, prob_emp[l], fabs(prob_emp[l] - prob_theo));
    }

    printf("\nVerified Result: q = %.1f -> Matches Option (i) 0.1\n", q_from_l0);

    return EXIT_SUCCESS;
}
