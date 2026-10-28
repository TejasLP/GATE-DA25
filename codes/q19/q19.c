#include <stdio.h>
#include <math.h>

int main() {
    // Array of progressively larger values of t approaching +infinity
    double t_values[] = {1e2, 1e4, 1e6, 1e8, 1e10, 1e12, 1e15};
    int num_values = sizeof(t_values) / sizeof(t_values[0]);

    printf("Verifying lim_{t -> +inf} (sqrt(t^2 + t) - t) = 0.5\n");
    printf("-------------------------------------------------------------------\n");
    printf("%-15s %-22s %-22s\n", "t value", "Computed Value", "Absolute Error");
    printf("-------------------------------------------------------------------\n");

    for (int i = 0; i < num_values; i++) {
        double t = t_values[i];
        
        // Direct evaluation of the limit expression
        double computed_val = sqrt(t * t + t) - t;
        
        // Difference from the expected limit value (0.5)
        double error = fabs(computed_val - 0.5);

        printf("%-15.0e %-22.12f %-22.12e\n", t, computed_val, error);
    }

    printf("-------------------------------------------------------------------\n");
    return 0;
}
