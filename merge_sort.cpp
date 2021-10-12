#include <bits/stdc++.h>
using namespace std;

void merge(int arr[], int left, int mid, int right)
{
    int brr[right + 1];
    int i = left;
    int j = mid + 1;
    int k = left;
    while (i <= mid && j <= right)
    {
        if (arr[i] < arr[j])
        {
            brr[k] = arr[i];
            i++;
        }
        else
        {
            brr[k] = arr[j];
            j++;
        }
        k++;
    }

    if (i > mid)
    {
        while (j <= right)
        {
            brr[k] = arr[j];
            k++;
            j++;
        }
    }
    else
    {
        while (i <= mid)
        {
            brr[k] = arr[i];
            k++;
            i++;
        }
    }
    for (k = left; k <= right; k++)
    {
        arr[k] = brr[k];
    }
}

void mergeSort(int arr[], int left, int right)
{
    if (left < right)
    {
        int mid = (left + right) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

int main()
{
    int arr[] = {9, 4, 7, 6, 3, 1, 5};
    int n = sizeof(arr) / sizeof(arr[0]);

    cout << "Before sorting the array is: ";
    for (int i = 0; i < n; i++)
    {
        cout << arr[i] << " ";
    }

    mergeSort(arr, 0, n - 1);

    cout << "\nAfter sorting the array is: ";
    for (int i = 0; i < n; i++)
    {
        cout << arr[i] << " ";
    }
    return 0;
}