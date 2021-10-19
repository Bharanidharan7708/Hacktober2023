
#include<stdio.h>
#include<conio.h>
#include<stdlib.h>
struct node
{
int data;
struct node *next;
}*head,*mid,*last;
void createlist();
void insertfirst(int);
void insertlast(int);
void insertmiddle(int,int);
void delfirst();
void dellast();
void delmiddle(int);
void search();
void reverselist();
void printlist();
void main()
{
clrscr() ;
printf("-----SINGLE LINKED LIST-----\n");
printf("elements in the list are: ");
createlist();
printlist();

printf("\ninsert the element 100 at beginning\n");
insertfirst(100);
printlist();
printf("\n");

printf("\ninsert the element 200 at last\n");
insertlast(200);
printlist();
printf("\n");

printf("\ninsert the element 300 at the 3 position\n ");
insertmiddle(300,3);
printlist();
printf("\n");

printf("\ndeleting the first node\n" );
delfirst();
printlist();
printf("\n");

printf("\ndeleting the last node\n");
dellast();
printlist();
printf("\n");

printf("\ndeleting the node at position 3\n");
delmiddle(3);
printlist();
printf("\n");

printf("\nsearching of element\n");
search();
printf("\n");

printf("\nReversing the list\n");
reverselist();
printlist();

getch();
}
void createlist()
{
head=malloc(sizeof(struct node));
mid=malloc(sizeof(struct node));
last=malloc(sizeof(struct node));
head->data=10;
mid->data=20;
last->data=30;
head->next=mid;
mid->next=last;
last->next=NULL;
}
void insertfirst(int x)
{
struct node *newnode=malloc(sizeof(struct node));
newnode->data=x;
newnode->next=head;
head=newnode;
}
void insertlast(int x)
{
struct node *newnode=malloc(sizeof(struct node));
newnode->data=x;
newnode->next=NULL;
if(head==NULL)
{
head=newnode;
}
else
{
struct node *temp;
temp=head;
while(temp->next!=NULL)
{
temp=temp->next;
}
temp->next=newnode;
}
}
void insertmiddle(int x,int pos)
{
int i;
struct node *temp;
struct node *newnode=malloc(sizeof(struct node));
newnode->data=x;
newnode->next=NULL;
temp=head;
for(i=1;i<pos-1;i++)
{
temp=temp->next;
if(temp==NULL)
{
break;
}
}
if(temp!=NULL)
{
newnode->next=temp->next;
temp->next=newnode;
}
else{
printf("\nthe position does not exist\n");
}
}
void delfirst()
{
struct node *todelete=head;
printf("data deleted is: %d\n",todelete->data);
if(head==NULL)
{
printf("list is empty");
}
else
{
head=head->next;
free(todelete);
}
}
void dellast()
{
struct node *todelete=head;
struct node *prevnode;
if(head==NULL)
{
printf("the list is empty cannot delete");
}
else
{
while(todelete->next!=NULL)
{
prevnode=todelete;
todelete=todelete->next;
}
printf("element to be deleted:%d\n",todelete->data);
prevnode->next=NULL;
free(todelete);
}
}
void delmiddle(int pos)
{
int i;
struct node *todelete,*prevnode;
todelete=head;
prevnode=head;
for(i=1;i<pos;i++)
{
prevnode=todelete;
todelete=todelete->next;
if(todelete==NULL)
{
break;
}
}
if(todelete->next!=NULL)
{
prevnode->next=todelete->next;
todelete->next=NULL;
free(todelete);
}
else
{
printf("the position does not exist");
}
}
void search()
{
struct node *temp;
int a,i=0,flag;
temp=head;
if(temp==NULL)
{
printf("the list is empty");
}
else
{
printf("\nenter the element to be searched:\n");
scanf("%d",&a);
while(temp!=NULL)
{
if(temp->data==a)
{
printf("element found at location:%d",i+1);
flag=0;
}
else
{
flag=1;
}
i++;
temp=temp->next;
}
}
if(flag==1)
{
printf("the element not found");

}
}
void reverselist()
{
struct node *prev,*current,*next;
current=head;
prev=NULL;
while(current!=NULL)
{
next=current->next;
current->next=prev;
prev=current;
current=next;
}
head=prev;
}
void printlist()
{
struct node*temp=head;
while(temp!=NULL)
{
printf("%d->",temp->data);
temp=temp->next;
}
}