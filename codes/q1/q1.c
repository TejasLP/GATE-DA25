#include <stdio.h>

int main() {
    // Define the 4x4 pixel intensity grid (U) as given in Fig. 1.2.1.1
    int U[4][4] = {
        {0, 1, 0, 2},
        {4, 7, 3, 3},
        {5, 5, 4, 4},
        {6, 7, 3, 2}
    };

    int threshold = 4;
    int count = 0;

    // Iterate through each row (i) and column (j) of the 4x4 grid
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            // Check the condition: U[i][j] <= 4
            // This implements the indicator function sum seen in the solution.
            if (U[i][j] <= threshold) {
                count++;
            }
        }
    }

    // Print the verification results to the console
    printf("=========================================================\n");
    printf("   Verification for Problem 1.2.1 (Pixels with U <= 4)   \n");
    printf("=========================================================\n");
    printf("Threshold Value    : %d\n", threshold);
    printf("Calculated Count   : %d\n", count);
    printf("Correct Option     : iii) 11\n");
    printf("=========================================================\n");

    return 0;
}
