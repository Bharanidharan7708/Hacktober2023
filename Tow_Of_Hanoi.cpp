#include <iostream>
using namespace std;
void hanoi_tow(int n, char src_rod, char dest_rod, char aux_rod){
    /*Here it depicts that the disk is moved from source to destination using auxiliary. 
    Whatever rod is taken in argumnets in first two positions depict source and destination respectively*/
    if (n == 1){
        cout << "\n Move disk 1 from rod " << src_rod << " to rod " << dest_rod;
        return;
    }
    hanoi_tow(n-1, src_rod, aux_rod, dest_rod);
    cout << "\n Move disk " << n << " from rod " << src_rod << " to rod " << dest_rod;
    hanoi_tow(n-1, aux_rod, dest_rod, src_rod);
}

int main(){
    int n;
    cout << "Enter the number of disks: ";
    cin >> n;
    hanoi_tow(n, 'A', 'C', 'B');  
    return 0;
}