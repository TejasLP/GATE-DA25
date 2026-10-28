#include <stdio.h>

// Function to simulate insertion sort and return the total number of swaps
int count_insertion_sort_swaps(int arr[], int n) {
    int swaps = 0;
    for (int i = 1; i < n; i++) {
        int j = i;
        // Insertion sort using adjacent swaps
        while (j > 0 && arr[j - 1] > arr[j]) {
            int temp = arr[j];
            arr[j] = arr[j - 1];
            arr[j - 1] = temp;
            swaps++;
            j--;
        }
    }
    return swaps;
}

int main() {
    // Given base array structure with a placeholder for x at index 6
    // Array: [1, 3, 5, 7, 9, 11, x, 15, 13]
    int base_array[] = {1, 3, 5, 7, 9, 11, 0, 15, 13};
    int n = sizeof(base_array) / sizeof(base_array[0]);

    // Options to test for x
    int options[] = {10, 12, 14, 16};
    int num_options = sizeof(options) / sizeof(options[0]);

    printf("Verifying options for x in [1, 3, 5, 7, 9, 11, x, 15, 13]:\n");

    for (int k = 0; k < num_options; k++) {
        int x = options[k];
        
        // Create a copy of the base array for each test
        int current_arr[9];
        for (int i = 0; i < n; i++) {
            current_arr[i] = base_array[i];
        }
        
        // Insert x into index 6
        current_arr[6] = x;

        // Count swaps required to sort
        int swaps = count_insertion_sort_swaps(current_arr, n);

        printf("Option %c) x = %2d -> Total Swaps = %d %s\n", 
               'i' + k, x, swaps, (swaps == 2) ? "<-- MATCH (Exactly 2 swaps)" : "");
    }

    return 0;
}
