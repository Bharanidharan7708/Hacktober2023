#include<iostream>
using namespace std;

struct Node{
    int data;
    Node *link;
};

int size = 0;

Node *top = NULL;

bool isempty(){
    if(top == NULL) return true;
    else return false;
}

void push(int value){
    // Initializing a new node
    Node *ptr = new Node();
    // Giving it a value
    ptr->data = value;
    // We then are making it point to the first element of the stack currently
    ptr->link = top;
    // Then we are making the current node the top
    top = ptr;
    size = size + 1;
}

void pop(){
    if (isempty()) cout<<"Stack is empty"<<endl;
    else{
        Node *ptr = top;
        top = top->link;
        delete(ptr);
        size = size - 1;
    }
}

void showTop(){
    if (isempty()) cout<<"Stack is empty"<<endl;
    else cout<<"Element at the top is "<<top->data<<endl;
}

int main(){
    cout<<size<<endl;
    push(5);
    showTop();
    cout<<size<<endl;
    push(10);
    push(5);
    cout<<size<<endl;
    push(10);
    showTop();
    pop();
    showTop();
    cout<<size<<endl;
    pop();
    showTop();
    cout<<size<<endl;
    return 0;
}
