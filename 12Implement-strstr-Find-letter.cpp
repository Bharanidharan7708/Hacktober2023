// 12 // find the position of the letter between the string.
#include<iostream>
using namespace std;
int main()
{
    string str, str2;
    cout << "\nEnter a alphabet string :  ";
    getline(cin, str);
    cout << "\nWhich letter or word you want to find :  ";
    getline(cin, str2);

    cout << endl << str.find(str2) << endl << endl;
}