#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Define structures for the relations
typedef struct {
    char model[20];
    int year;
    int serial;
    char color[20];
} Car;

typedef struct {
    char maker[20];
    char model[20];
} Make;

typedef struct {
    char owner[20];
    int serial;
} Own;

// Helper structure for intermediate join results: Car + Make info
typedef struct {
    char model[20];
    int year;
    int serial;
    char color[20];
    char maker[20];
} CarMake;

// Helper structure for final joined records with Owner info
typedef struct {
    char owner[20];
    char model[20];
    int year;
    int serial;
    char color[20];
    char maker[20];
} FullRecord;

int main() {
    printf("=========================================================\n");
    printf("     Relational Algebra Simulation in C (Problem 1.2.9)  \n");
    printf("=========================================================\n\n");

    // --- 1. ARBITRARY INPUT DATA ---
    
    // Relation: Make (maker, model)
    Make makes[] = {
        {"ABC", "Civic"},
        {"XYZ", "Corolla"},
        {"ABC", "ModelS"},
        {"DEF", "Mustang"},
        {"ABC", "Accord"}
    };
    int num_makes = 5;

    // Relation: Car (model, year, serial, color)
    Car cars[] = {
        {"Civic", 2021, 101, "red"},
        {"Corolla", 2022, 102, "blue"},
        {"ModelS", 2023, 103, "red"},
        {"Mustang", 2020, 104, "red"},
        {"Accord", 2022, 105, "black"},
        {"Civic", 2023, 106, "white"}
    };
    int num_cars = 6;

    // Relation: Own (owner, serial)
    Own owns[] = {
        {"Alice", 101},
        {"Bob", 102},
        {"Charlie", 103},
        {"Alice", 104},
        {"David", 105},
        {"Eve", 106}
    };
    int num_owns = 6;

    // --- 2. OPERATION 1: Selection on Make -> σ_maker='ABC'(Make) ---
    printf("Step 1: Selecting makers where maker = 'ABC'...\n");
    Make filtered_makes[10];
    int num_filtered_makes = 0;
    for (int i = 0; i < num_makes; i++) {
        if (strcmp(makes[i].maker, "ABC") == 0) {
            filtered_makes[num_filtered_makes++] = makes[i];
            printf("  -> Found: Maker = %s, Model = %s\n", makes[i].maker, makes[i].model);
        }
    }
    printf("\n");

    // --- 3. OPERATION 2: Natural Join -> Car ⨝ (σ_maker='ABC' Make) on 'model' ---
    printf("Step 2: Natural Join of Car and Filtered Make on 'model'...\n");
    CarMake car_make_join[20];
    int num_car_make = 0;
    for (int i = 0; i < num_cars; i++) {
        for (int j = 0; j < num_filtered_makes; j++) {
            if (strcmp(cars[i].model, filtered_makes[j].model) == 0) {
                strcpy(car_make_join[num_car_make].model, cars[i].model);
                car_make_join[num_car_make].year = cars[i].year;
                car_make_join[num_car_make].serial = cars[i].serial;
                strcpy(car_make_join[num_car_make].color, cars[i].color);
                strcpy(car_make_join[num_car_make].maker, filtered_makes[j].maker);
                
                printf("  -> Joined: [%s, %d, Serial:%d, Color:%s, Maker:%s]\n", 
                       car_make_join[num_car_make].model, car_make_join[num_car_make].year, 
                       car_make_join[num_car_make].serial, car_make_join[num_car_make].color, 
                       car_make_join[num_car_make].maker);
                num_car_make++;
            }
        }
    }
    printf("\n");

    // --- 4. OPERATION 3: Selection -> σ_color='red'(Car ⨝ Make) ---
    printf("Step 3: Selecting records where color = 'red'...\n");
    CarMake red_abc_cars[20];
    int num_red_abc = 0;
    for (int i = 0; i < num_car_make; i++) {
        if (strcmp(car_make_join[i].color, "red") == 0) {
            red_abc_cars[num_red_abc++] = car_make_join[i];
            printf("  -> Filtered Red ABC Car: Model=%s, Serial=%d\n", 
                   car_make_join[i].model, car_make_join[i].serial);
        }
    }
    printf("\n");

    // --- 5. OPERATION 4: Natural Join -> Own ⨝ (Red ABC Cars) on 'serial' ---
    printf("Step 4: Natural Join with 'Own' relation on 'serial'...\n");
    FullRecord final_matches[20];
    int num_final = 0;
    for (int i = 0; i < num_owns; i++) {
        for (int j = 0; j < num_red_abc; j++) {
            if (owns[i].serial == red_abc_cars[j].serial) {
                strcpy(final_matches[num_final].owner, owns[i].owner);
                final_matches[num_final].serial = owns[i].serial;
                strcpy(final_matches[num_final].model, red_abc_cars[j].model);
                final_matches[num_final].year = red_abc_cars[j].year;
                strcpy(final_matches[num_final].color, red_abc_cars[j].color);
                strcpy(final_matches[num_final].maker, red_abc_cars[j].maker);
                
                printf("  -> Match Found: Owner=%s owns Red ABC Car (Serial:%d, Model:%s)\n",
                       final_matches[num_final].owner, final_matches[num_final].serial, 
                       final_matches[num_final].model);
                num_final++;
            }
        }
    }
    printf("\n");

    // --- 6. OPERATION 5: Projection -> π_owner(Final Matches) ---
    printf("Step 5: Projecting owners (π_owner)...\n");
    printf("=========================================================\n");
    printf(" FINAL OUTPUT (Owners of a red car made by ABC):\n");
    printf("=========================================================\n");
    
    // Print unique owners to avoid duplicate printing if an owner has multiple matching cars
    for (int i = 0; i < num_final; i++) {
        bool duplicate = false;
        for (int k = 0; k < i; k++) {
            if (strcmp(final_matches[i].owner, final_matches[k].owner) == 0) {
                duplicate = true;
                break;
            }
        }
        if (!duplicate) {
            printf(" * Owner: %s\n", final_matches[i].owner);
        }
    }
    printf("=========================================================\n");

    return 0;
}
