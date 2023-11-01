#include <iostream>
using namespace std;

void inputArray(int arr[], int size) {
    cout << "Enter " << size << " numbers randomly: " << endl;
    for (int i = 0; i < size; i++) {
        cin >> arr[i];
    }
}

void displayArray(int arr[], int size) {
    cout << "Input array is: " << endl;
    for (int i = 0; i < size; i++) {
        cout << "\t\t\tValue at " << i << " Index: " << arr[i] << endl;
    }
}

void bubbleSort(int arr[], int size) {
    int temp;
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

void displaySortedArray(int arr[], int size) {
    cout << "Sorted Array is: " << endl;
    for (int i = 0; i < size; i++) {
        cout << "\t\t\tValue at " << i << " Index: " << arr[i] << endl;
    }
}

int main() {
    int array[5];
    const int size = 5;

    inputArray(array, size);
    cout << endl;
    displayArray(array, size);

    bubbleSort(array, size);

    cout << endl;
    displaySortedArray(array, size);

    return 0;
}

