#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_STR 32
#define MAX_ROWS 32

// ---------------------------------------------------------
// 1. Struct Definitions
// ---------------------------------------------------------

// Tuple for Loan table
typedef struct {
    char loan_num[MAX_STR];
    char branch_name[MAX_STR];
    int amount;
} Loan;

// Tuple for Borrower table
typedef struct {
    char customer_name[MAX_STR];
    char loan_num[MAX_STR];
} Borrower;

// Tuple for Joined relation: (customer_name, branch_name)
typedef struct {
    char customer_name[MAX_STR];
    char branch_name[MAX_STR];
} JoinedRelation;

// ---------------------------------------------------------
// 2. Data Initialization
// ---------------------------------------------------------

Loan loan_table[] = {
    {"L11", "Banjara Hills", 90000},
    {"L14", "Kondapur",      50000},
    {"L15", "SR Nagar",      40000},
    {"L22", "SR Nagar",      25000},
    {"L23", "Balanagar",     80000},
    {"L25", "Kondapur",      70000},
    {"L19", "SR Nagar",      65000}
};
int loan_count = sizeof(loan_table) / sizeof(loan_table[0]);

Borrower borrower_table[] = {
    {"Anand",   "L11"},
    {"Karteek", "L11"},
    {"Karteek", "L14"},
    {"Ankita",  "L15"},
    {"Gopal",   "L19"},
    {"Karteek", "L22"},
    {"Karteek", "L23"},
    {"Sunil",   "L23"},
    {"Sunil",   "L25"}
};
int borrower_count = sizeof(borrower_table) / sizeof(borrower_table[0]);

// ---------------------------------------------------------
// 3. Relational Algebra Operations
// ---------------------------------------------------------

// Performs Natural Join: Loan <x> Borrower and Projects (branch_name, customer_name)
int perform_natural_join_and_projection(JoinedRelation result[]) {
    int count = 0;
    for (int i = 0; i < loan_count; i++) {
        for (int j = 0; j < borrower_count; j++) {
            if (strcmp(loan_table[i].loan_num, borrower_table[j].loan_num) == 0) {
                // Check for duplicate (customer_name, branch_name) pairs to ensure distinct projection
                bool exists = false;
                for (int k = 0; k < count; k++) {
                    if (strcmp(result[k].customer_name, borrower_table[j].customer_name) == 0 &&
                        strcmp(result[k].branch_name, loan_table[i].branch_name) == 0) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    strcpy(result[count].customer_name, borrower_table[j].customer_name);
                    strcpy(result[count].branch_name, loan_table[i].branch_name);
                    count++;
                }
            }
        }
    }
    return count;
}

// Gets unique branches from Loan table: \pi_{branch_name}(Loan)
int get_unique_branches(char branches[][MAX_STR]) {
    int count = 0;
    for (int i = 0; i < loan_count; i++) {
        bool exists = false;
        for (int j = 0; j < count; j++) {
            if (strcmp(branches[j], loan_table[i].branch_name) == 0) {
                exists = true;
                break;
            }
        }
        if (!exists) {
            strcpy(branches[count], loan_table[i].branch_name);
            count++;
        }
    }
    return count;
}

// Gets unique customers from joined relation
int get_unique_customers(JoinedRelation joined[], int joined_count, char customers[][MAX_STR]) {
    int count = 0;
    for (int i = 0; i < joined_count; i++) {
        bool exists = false;
        for (int j = 0; j < count; j++) {
            if (strcmp(customers[j], joined[i].customer_name) == 0) {
                exists = true;
                break;
            }
        }
        if (!exists) {
            strcpy(customers[count], joined[i].customer_name);
            count++;
        }
    }
    return count;
}

// ---------------------------------------------------------
// 4. Main Function & Division Execution
// ---------------------------------------------------------

int main() {
    JoinedRelation joined[MAX_ROWS];
    char unique_branches[MAX_ROWS][MAX_STR];
    char unique_customers[MAX_ROWS][MAX_STR];

    int joined_count = perform_natural_join_and_projection(joined);
    int branch_count = get_unique_branches(unique_branches);
    int customer_count = get_unique_customers(joined, joined_count, unique_customers);

    printf("=== UNIQUE BRANCHES IN LOAN TABLE (%d total) ===\n", branch_count);
    for (int i = 0; i < branch_count; i++) {
        printf(" - %s\n", unique_branches[i]);
    }

    printf("\n=== RELATIONAL DIVISION RESULT ===\n");
    int division_tuples = 0;

    // Relational Division: Find customer connected to ALL unique branches
    for (int i = 0; i < customer_count; i++) {
        bool has_all_branches = true;

        for (int j = 0; j < branch_count; j++) {
            bool found_pair = false;
            for (int k = 0; k < joined_count; k++) {
                if (strcmp(joined[k].customer_name, unique_customers[i]) == 0 &&
                    strcmp(joined[k].branch_name, unique_branches[j]) == 0) {
                    found_pair = true;
                    break;
                }
            }
            if (!found_pair) {
                has_all_branches = false;
                break;
            }
        }

        if (has_all_branches) {
            printf(" Matching Customer: %s\n", unique_customers[i]);
            division_tuples++;
        }
    }

    printf("\nTotal number of tuples returned: %d\n", division_tuples);
    return 0;
}
