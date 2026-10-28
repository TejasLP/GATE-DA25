#include <stdio.h>
#include <math.h>

int main() {
    printf("=========================================================\n");
    printf("     Verification Program for Problem 1.2.2 Options      \n");
    printf("=========================================================\n\n");

    // Define multiple test cases where Length (L) > Width (W)
    double lengths[] = {10.0, 25.0, 15.0, 50.0};
    double widths[]  = {5.0,  10.0, 8.0,  20.0};
    int num_cases = 4;

    for (int c = 0; c < num_cases; c++) {
        double L = lengths[c];
        double W = widths[c];
        
        // 1. Original properties of the rectangle
        double P = 2 * (L + W);                  // Perimeter
        double D = sqrt(L * L + W * W);          // Diagonal length
        double A = L * W;                        // Area

        // 2. Modified properties (Width increased by 10%, i.e., W' = 1.10 * W)
        double W_new = 1.10 * W;
        double P_new = 2 * (L + W_new);
        double D_new = sqrt(L * L + W_new * W_new);
        double A_new = L * W_new;

        // 3. Calculate percentage changes for each property
        double p_change = ((P_new - P) / P) * 100.0;
        double d_change = ((D_new - D) / D) * 100.0;
        double a_change = ((A_new - A) / A) * 100.0;

        // 4. Print results for the current test case
        printf("Test Case %d: Initial L = %.1f, W = %.1f\n", c + 1, L, W);
        printf("  [i] Perimeter increase : %.2f%% (False, varies by L and W)\n", p_change);
        printf("  [ii] Diagonal increase : %.2f%% (False, varies by L and W)\n", d_change);
        printf("  [iii] Area increase    : %.2f%% (True, exactly 10.00%% for all L, W)\n", a_change);
        printf("  [iv] Becomes a square  : %s (False, L equals W_new only by coincidence)\n", (fabs(L - W_new) < 1e-5) ? "True" : "False");
        printf("---------------------------------------------------------\n");
    }

    printf("\nFinal Conclusion:\n");
    printf("Option (iii) is the only statement that is universally true\n");
    printf("for all values of L and W.\n");

    return 0;
}
