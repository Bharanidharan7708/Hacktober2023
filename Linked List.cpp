//----------------Linked List-----------------//
//-----Traversal--Insertion--Deletion---------//

#include<bits/stdc++.h>
using namespace std;

class node{
    public: 
    int data;
    node* next;

    node(){
        data=0;
        next=NULL;
    }
    node(int tmp){
        data=tmp;
        next=NULL;
    }
};

class linkedlist {
    node* head;
    public:
    linkedlist(){
        head=NULL;
    }
    void insert_node(int data);

    void display ();
    
    void delete_node(int key);
};

void linkedlist::insert_node(int data){
    node* new_node= new node(data);
    if(head==NULL){
        head=new_node;
        return;
    }

    node* temp=head;
    while(temp->next!=NULL){
        temp=temp->next;
    }
    temp->next=new_node;
}
//to delete specified node 
void linkedlist::delete_node(int key){
    node *temp=head, *prev=NULL;
     
    if(temp!=NULL && temp->data==key){
        head=temp->next;
        delete temp;
        return;
    }

    while(temp!=NULL && temp->data!=key){
        prev=temp;
        temp=temp->next;
    }
    if(temp==NULL){
        cout<<"ERROR: key not found\n";
        delete temp;
        return;
    }
    prev->next=temp->next;
    delete temp;
    return;
}

void linkedlist::display (){
    node* temp=head;
    if(head==NULL){
        cout<<"list is empty\n";
        return;
    }
    while(temp!=NULL){
        cout<<temp->data<<" ";
        temp=temp->next;
    }
}


int main(){
    //declaring object
    linkedlist l;

    //taking input
    cout<<"Enter no of nodes you want to insert\n";
    int len;
    cin>>len;
    cout<<"Enter data\n";
    for(int i=0;i<len;i++){
        int tmp;
        cin>>tmp;
        l.insert_node(tmp);
    }

    //output data
    cout<<"\nData you have entered is:\n";
    l.display();
    
    //deletion
    cout<<"\n\nEnter no of nodes you want to delete\n";
    int n=-1;
    do{
        if(n>len){
            cout<<"\nERROR:Kindly enter valid input--";
        }
        cin>>n;
    }
    while(n>len);
    
    while(n--){
        cout<<"\n\nEnter node data you want to delete: ";
        int count;
        cin>>count;
        l.delete_node(count);
    }
    
    //display after deletion
    cout<<"\nData after deletion is:\n";
    l.display();

    return 0;
}