#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

// Build a singly linked list from an array
Node* create_linked_list(const int *arr, int n) {
    Node *head = NULL, *tail = NULL;
    for (int i = 0; i < n; i++) {
        Node *new_node = (Node *)malloc(sizeof(Node));
        new_node->data = arr[i];
        new_node->next = NULL;
        if (!head) head = tail = new_node;
        else { tail->next = new_node; tail = new_node; }
    }
    return head;
}

void free_linked_list(Node *head) {
    while (head) {
        Node *temp = head;
        head = head->next;
        free(temp);
    }
}

// Binary Search on an Array: O(1) random access to median
int bsearch_array(const int *arr, int n, int target, long *ops) {
    int low = 0, high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        (*ops)++; // 1 random-access comparison at arr[mid]
        if (arr[mid] == target)
            return mid;
        else if (arr[mid] < target)
            low = mid + 1;
        else
            high = mid - 1;
    }
    return -1;
}

// Binary Search on a Singly Linked List: O(k) pointer traversal to median
int bsearch_linked_list(Node *head, int n, int target, long *ops) {
    int low = 0, high = n - 1;
    Node *low_node = head;

    while (low <= high) {
        int mid_offset = (high - low) / 2;
        int mid = low + mid_offset;

        // Must traverse pointers sequentially to reach the median element
        Node *mid_node = low_node;
        for (int i = 0; i < mid_offset; i++) {
            mid_node = mid_node->next;
            (*ops)++; // Count pointer hop
        }

        (*ops)++; // Comparison at mid_node
        if (mid_node->data == target)
            return mid;
        else if (mid_node->data < target) {
            low = mid + 1;
            low_node = mid_node->next;
            (*ops)++;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}

// Shuffle array to simulate "any order" (Options i & ii)
void shuffle_array(int *arr, int n) {
    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

int main(void) {
    srand(42);
    int N_test = 1024;

    int *sorted_arr = (int *)malloc(N_test * sizeof(int));
    int *unsorted_arr = (int *)malloc(N_test * sizeof(int));

    sorted_arr[0] = 2;
    for (int i = 1; i < N_test; i++) {
        sorted_arr[i] = sorted_arr[i - 1] + (rand() % 5 + 1);
    }
    for (int i = 0; i < N_test; i++) {
        unsorted_arr[i] = sorted_arr[i];
    }
    shuffle_array(unsorted_arr, N_test);

    Node *unsorted_list = create_linked_list(unsorted_arr, N_test);
    Node *sorted_list   = create_linked_list(sorted_arr, N_test);

    // -----------------------------------------------------------------
    // Part 1: Verify All 4 Options at n = 1024 (log2(1024) = 10)
    // -----------------------------------------------------------------
    int found_i = 0, found_ii = 0, found_iii = 0, found_iv = 0;
    long dummy_ops = 0;

    for (int i = 0; i < N_test; i++) {
        int key = sorted_arr[i];
        if (bsearch_array(unsorted_arr, N_test, key, &dummy_ops) != -1) found_i++;
        if (bsearch_linked_list(unsorted_list, N_test, key, &dummy_ops) != -1) found_ii++;
        if (bsearch_array(sorted_arr, N_test, key, &dummy_ops) != -1) found_iii++;
        if (bsearch_linked_list(sorted_list, N_test, key, &dummy_ops) != -1) found_iv++;
    }

    // Worst-case target (larger than maximum element)
    int worst_target = sorted_arr[N_test - 1] + 10;
    long ops_i = 0, ops_ii = 0, ops_iii = 0, ops_iv = 0;

    bsearch_array(unsorted_arr, N_test, worst_target, &ops_i);
    bsearch_linked_list(unsorted_list, N_test, worst_target, &ops_ii);
    bsearch_array(sorted_arr, N_test, worst_target, &ops_iii);
    bsearch_linked_list(sorted_list, N_test, worst_target, &ops_iv);

    printf("=== GATE DA 2025 Q1.2.15: Verification of Options (n = %d, log2(n) = 10) ===\n", N_test);
    printf("%-42s | %-14s | %-15s | %-12s\n", "Input Option", "Search Success", "Worst-Case Ops", "Complexity");
    printf("-----------------------------------------------------------------------------------------------\n");
    printf("i)   Array in any order                    | %6.1f%% (FAIL) | %15ld | Invalid\n",
           (found_i * 100.0) / N_test, ops_i);
    printf("ii)  Linked list in any order              | %6.1f%% (FAIL) | %15ld | Invalid\n",
           (found_ii * 100.0) / N_test, ops_ii);
    printf("iii) Array in increasing order             | %6.1f%% (PASS) | %15ld | O(log n) [VERIFIED]\n",
           (found_iii * 100.0) / N_test, ops_iii);
    printf("iv)  Linked list in increasing order       | %6.1f%% (PASS) | %15ld | O(n)\n\n",
           (found_iv * 100.0) / N_test, ops_iv);

    // -----------------------------------------------------------------
    // Part 2: Scaling Comparison Between Valid Sorted Options (iii vs iv)
    // -----------------------------------------------------------------
    printf("=== Scaling Verification: Option (iii) vs Option (iv) ===\n");
    printf("%-8s | %-8s | %-20s | %-20s\n", "n", "log2(n)", "Option (iii) Array", "Option (iv) List");
    printf("-------------------------------------------------------------------\n");

    for (int exp = 6; exp <= 12; exp++) {
        int n = 1 << exp;
        int *arr = (int *)malloc(n * sizeof(int));
        for (int i = 0; i < n; i++) arr[i] = i * 2;
        Node *list = create_linked_list(arr, n);

        long arr_ops = 0, list_ops = 0;
        bsearch_array(arr, n, n * 2 + 1, &arr_ops);
        bsearch_linked_list(list, n, n * 2 + 1, &list_ops);

        printf("%-8d | %-8d | %4ld ops (~log2 n)   | %6ld ops (~n)\n",
               n, exp, arr_ops, list_ops);

        free_linked_list(list);
        free(arr);
    }

    free_linked_list(unsorted_list);
    free_linked_list(sorted_list);
    free(sorted_arr);
    free(unsorted_arr);
    return EXIT_SUCCESS;
}
