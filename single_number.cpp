#include<iostream>
using namespace std;
int main()
{
  int n;
  cin>>n;
  // ex : [1,2,1,2,3] -> ans = 3 -> In an array one number occurs once and all other number twice
  // ex : [1,2,3,1,3,2,4] -> ans = 4 
  int xor =0;
  int arr[n];
  for(int i=0;i<n;i++)
  {
    xor = xor ^ arr[i];
  }
  cout<<xor<<endl;
  
  
  
}
