#include<iostream>
#include<bits/stdc++.h>
using namespace std;
int lcs(int array[],int n)
{
    vector<int> temp;
    temp.push_back(array[0]);
    for(int i=1;i<n;i++)
    {
        if(array[i]>temp.back())
        temp.push_back(array[i]);
        else
        {
            int x = lower_bound(temp.begin(),temp.end(),array[i])-temp.begin();
            temp[x] = array[i];
        }
    }
    return temp.size();
}
int main()
{
    int n;
    cout << "Array Size:";
    cin >> n;
    int array[n];
    cout << "Enter array elements : ";
    for(int i=0;i<n;i++)
    cin >> array[i];
    cout << "Length of longest increasing subsequence : " << lcs(array,n);
    return 0;
}