#include<iostream>
#include<cstdlib>
#include<time.h>
using namespace std;

int main(void)
{
	cout<<"*************************** WELCOME TO MY GAME ***********************\n";
	
	srand((unsigned)time(NULL));
	int mynum; 
    mynum=1+(rand()%100);
    cout<<"\n GUESS MY NUMBER (1-100): "; 
    int num=0;
    
    do{
    	
        cin>>num;
        if(mynum==num)
        {
			cout<<"\n Congratulation......Correct Guess!!!!! ";
            break;
        }
        else if(mynum<num)
        {
            cout<<"\n Your number is larger than my number ";
        }
        else
        {
            cout<<"\n Your number is smaller than my number ";
        }
        cout<<"\n try again ";
            
    }while(num>=0);    

	cout<<"\n My number was : "<<mynum;     

return 0;
}

/*  OUTPUT  
*************************** WELCOME TO MY GAME ***********************

 GUESS MY NUMBER (1-100): 50

 Your number is larger than my number
 try again 40

 Your number is larger than my number
 try again 30

 Your number is smaller than my number
 try again 35

 Congratulation......Correct Guess!!!!!
 My number was : 35
 
 */
