#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define N 1000000  // Number of Monte Carlo samples

int main() {
    srand(42); // Seed for reproducibility

    // Define the 4 options for lambda from the problem:
    // i) ln 2, ii) ln 4, iii) ln 3, iv) ln 0.25
    double lambdas[4] = {
        log(2.0),
        log(4.0),
        log(3.0),
        log(0.25)
    };
    
    const char* option_labels[4] = {
        "i)   ln 2    (~0.6931)",
        "ii)  ln 4    (~1.3863)",
        "iii) ln 3    (~1.0986)",
        "iv)  ln 0.25 (~-1.3863)"
    };

    printf("========================================================================================\n");
    printf("%-25s | Lambda Value | Estimated Pr(X >= 2) (Target: 0.25)\n", "Option");
    printf("========================================================================================\n");

    for (int k = 0; k < 4; k++) {
        double lambda = lambdas[k];
        
        // Rate parameter lambda must be strictly positive for a valid exponential distribution
        if (lambda <= 0) {
            printf("%-25s | %12.4f | Invalid (lambda must be > 0)\n", option_labels[k], lambda);
            continue;
        }

        int count_ge_2 = 0;

        for (int i = 0; i < N; i++) {
            // Generate U uniformly distributed on (0, 1]
            double u = (double)rand() / ((double)RAND_MAX + 1.0);
            while (u == 0.0) { // Prevent log(0)
                u = (double)rand() / ((double)RAND_MAX + 1.0);
            }

            // Inverse transform sampling: X = -ln(U) / lambda
            double x = -log(u) / lambda;

            if (x >= 2.0) {
                count_ge_2++;
            }
        }

        double prob = (double)count_ge_2 / N;
        printf("%-25s | %12.4f | %32.4f\n", option_labels[k], lambda, prob);
    }

    printf("========================================================================================\n");
    return 0;
}
