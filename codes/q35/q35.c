#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUM_SIMULATIONS 100000 // Total Monte Carlo experiment trials

// Function to generate a random Bernoulli variable X ~ Bernoulli(p)
int toss_coin(double p) {
    double r = (double)rand() / RAND_MAX;
    return (r < p) ? 1 : 0;
}

// Computes sample mean (E[p_hat]) and sample variance (Var(p_hat)) for a given n
void run_simulation(int n, double p, double *expected_p_hat, double *var_p_hat) {
    double p_hat_samples[NUM_SIMULATIONS];
    double sum_p_hat = 0.0;

    // Perform Monte Carlo simulations
    for (int sim = 0; sim < NUM_SIMULATIONS; sim++) {
        int heads_count = 0;
        for (int i = 0; i < n; i++) {
            heads_count += toss_coin(p);
        }
        
        // p_hat = (1/n) * sum(X_i)
        double p_hat = (double)heads_count / n;
        p_hat_samples[sim] = p_hat;
        sum_p_hat += p_hat;
    }

    // Empirically estimate E[p_hat]
    double mean = sum_p_hat / NUM_SIMULATIONS;
    *expected_p_hat = mean;

    // Empirically estimate Var(p_hat)
    double sum_sq_diff = 0.0;
    for (int sim = 0; sim < NUM_SIMULATIONS; sim++) {
        double diff = p_hat_samples[sim] - mean;
        sum_sq_diff += diff * diff;
    }
    *var_p_hat = sum_sq_diff / (NUM_SIMULATIONS - 1);
}

int main() {
    // Seed the pseudo-random number generator
    srand((unsigned int)time(NULL));

    double p = 0.6; // Chosen probability of heads
    int n_values[] = {10, 50, 200, 1000}; // Increasing values of n
    int num_tests = sizeof(n_values) / sizeof(n_values[0]);

    printf("Theoretical values for p = %.2f:\n", p);
    printf("E[p_hat] = %.4f\n", p);
    printf("Theoretical Var(p_hat) = p*(1-p)/n\n\n");

    printf("%-8s | %-12s | %-14s | %-14s\n", "n", "Sim E[p_hat]", "Sim Var[p_hat]", "Theory Var[p_hat]");
    printf("-------------------------------------------------------------\n");

    for (int k = 0; k < num_tests; k++) {
        int n = n_values[k];
        double exp_p_hat, var_p_hat;

        run_simulation(n, p, &exp_p_hat, &var_p_hat);

        double theoretical_var = (p * (1.0 - p)) / n;

        printf("%-8d | %-12.4f | %-14.6f | %-14.6f\n", n, exp_p_hat, var_p_hat, theoretical_var);
    }

    return 0;
}
