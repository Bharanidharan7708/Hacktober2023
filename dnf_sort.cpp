#include <bits/stdc++.h>
using namespace std;

void dnfsort(int arr[], int n)
{
    int low = 0;
    int mid = 0;
    int high = n - 1;
    int temp;
    while (mid <= high)
    {
        switch (arr[mid])
        {
        case 0:
            temp = arr[low];
            arr[low] = arr[mid];
            arr[mid] = temp;
            low++;
            mid++;
            break;
        case 1:
            mid++;
            break;
        case 2:
            temp = arr[mid];
            arr[mid] = arr[high];
            arr[high] = temp;
            high--;
            break;
        }
    }
}

int main()
{
    int arr[] = {2, 0, 2, 1, 1, 0};
    int n = sizeof(arr) / sizeof(arr[0]);

    dnfsort(arr, n);
    cout << "DNFSort gives: ";
    for (int i = 0; i < n; i++)
    {
        cout << arr[i] << " ";
    }

    return 0;
}