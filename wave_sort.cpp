/* WaveSort means -> Given an array, transform the array such that
arr[0] >= arr[1] <= arr[2] >= arr[3] <= arr[4] >= …..
*/

#include <bits/stdc++.h>
using namespace std;

void swap(int arr[], int a, int b)
{
    int temp = arr[a];
    arr[a] = arr[b];
    arr[b] = temp;
}

void wavesort(int arr[], int n)
{
    for (int i = 1; i < n; i += 2)
    {
        if (arr[i] > arr[i - 1])
        {
            swap(arr, i, i - 1);
        }
        if (arr[i] > arr[i + 1] && i <= n - 2)
        {
            swap(arr, i, i + 1);
        }
    }
}

int main()
{
    int arr[] = {1, 3, 4, 7, 5, 6, 2};
    int n = sizeof(arr) / sizeof(arr[0]);

    wavesort(arr, n);
    cout << "WaveSort gives: ";
    for (int i = 0; i < n; i++)
    {
        cout << arr[i] << " ";
    }

    return 0;
}