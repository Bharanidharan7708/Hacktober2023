#include<bits/stdc++.h>
using namespace std;

void bubbleSort(int arr[], int n){
    
    bool swapped;
    for(int i = 0;i < n; i++){
        
        swapped = false; // initialising the variable as false, and will change it to true if swapping occurs.
        for(int j = 0 ; j < n - i -1; j++){
            if( arr[j] > arr[j+1]){
                swap(arr[j], arr[j+1]);
                swapped = true;
            }
        }
        
        if( swapped == false)
        break;
        // the loop will break if no swapping takes place
        // Hence making the time complexity O(n) in the best case which will occur if the given input array is already sorted.
    }
}

int main() {
	int a[] = {2, 1, 3, 4};
	bubbleSort(a, 4);
	for(int i = 0; i < 4; i++){
	    cout<<a[i]<<" ";
	}
	return 0;
}
