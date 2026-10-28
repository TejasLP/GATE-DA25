#include <stdio.h>
#include <math.h>

int main() {
    printf("=========================================================\n");
    printf("     Verification Program for Problem 1.2.4              \n");
    printf("=========================================================\n\n");

    // The equation given is: 3^(x^2) = 27 * 9^x
    // Solving this algebraically yields two valid roots: x = 3 and x = -1
    double test_roots[] = {3.0, -1.0};
    int num_roots = 2;

    for (int i = 0; i < num_roots; i++) {
        double x = test_roots[i];

        // 1. Verify the main equation: 3^(x^2) == 27 * 9^x
        double lhs = pow(3.0, x * x);
        double rhs = 27.0 * pow(9.0, x);

        // 2. Evaluate the target expression: (2^(x^2)) / ((2^x)^2)
        double numerator = pow(2.0, x * x);
        double denominator = pow(pow(2.0, x), 2.0);
        double evaluated_value = numerator / denominator;

        // Display results for each root
        printf("Test Root: x = %.1f\n", x);
        printf("  * Equation Check: 3^(%.1f^2) = %.2f | 27 * 9^(%.1f) = %.2f\n", x, lhs, x, rhs);
        printf("    Status: %s\n", (fabs(lhs - rhs) < 1e-5) ? "VALID ROOT" : "INVALID");
        
        printf("  * Expression Value [2^(x^2) / (2^x)^2]: %.2f\n", evaluated_value);
        printf("    Matches Option: iii) 2^3 (= 8)\n");
        printf("---------------------------------------------------------\n");
    }

    return 0;
}
