#include<stdio.h>
#include<stdlib.h>
struct node *head=NULL;
struct node
{
	struct node *previous;
	int data;
	struct node *next;
	
};
struct node *create(struct node *newnode,struct node *traverse);
void display(struct node *traverse);
void search(struct node *traverse);
void insert_beg(struct node *newnode);	
void insert_end(struct node *traverse,struct node *newnode);
void insert_location(struct node *traverse,struct node *newnode);
void delete_beg(struct node *traverse);
void delete_end(struct node *traverse);
void delete_location(struct node *traverse);
int main()
{ 
    int x,y;
    struct node *newnode=NULL,*traverse=NULL;
	do
	{
	printf("1.create  2.display  3.search  4.insert at begin   5.insert at end   6.insert at specific location   7.delete at begin    8.delete at end   9.delete at specific location");	
	printf("\nenter your choice:");
	scanf("%d",&y);
	switch(y)
	{
	case 1:printf("\ncreate your linked list");
			head=create(newnode,traverse);
	        break;
    case 2:display(traverse);
            break;
	case 3:search(traverse);
			break;
	case 4:insert_beg(newnode);
			break;
	case 5:insert_end(traverse,newnode);
			break;
	case 6:insert_location(traverse,newnode);
			break;
	case 7:delete_beg(traverse);
			break;
	case 8:delete_end(traverse);
			break;
	case 9:delete_location(traverse);
			break;
    default:printf("invalid choice");
			break;	
	}
	printf("\ndo you want to perform more operation :\n");
	printf("press 1 for yes\n 0 for no\n");
	scanf("%d",&x);
	}
	while(x);
	return 0;
}
struct node *create(struct node *newnode,struct node *traverse)
{
int choice;
	do
	{
		newnode=(struct node *)malloc(sizeof(struct node));
		newnode->previous=NULL;
		printf("\nenter the data:");
		scanf("%d",&newnode->data);
		newnode->next=NULL;
		if(head==NULL)
		{
			head=newnode;
			traverse=head;
		}
		else
		{
			traverse->next=newnode;
			newnode->previous=traverse;
			traverse=newnode;
		}
		printf("\ndata inserted:%d",newnode->data);
	    printf("\nenter more node:1.yes 0.no");
	    scanf("%d",&choice);
	}
	while(choice);
	return head;	
}
void display(struct node *traverse)
{
	traverse=head;
	printf("display all elements:\n");
	while(traverse!=NULL)
	{
	printf("%d\t",traverse->data);
	traverse=traverse->next;
	}
}
void search(struct node *traverse)
{
	traverse=head;
	int ele,count=1,flag=0;
	printf("\nenter the element to be search");
	scanf("%d",&ele);
	while(traverse!=NULL)
	{
		if(traverse->data==ele)
		{
	    	flag=1;
		    break;
		}
		else
		{
			traverse=traverse->next;
		}
		count++;
	}
	if(flag==0)
	printf("element not found");
	else if(flag==1)
	printf("element present at node %d",count);
}
void insert_beg(struct node *newnode)
{
	newnode=(struct node *)malloc(sizeof(struct node));
	printf("\nenter the data of new node:");
	scanf("%d",&newnode->data);
	newnode->next=NULL;
	newnode->previous=NULL;
	if(head==NULL)
	{
		head=newnode;
	}
	else
	newnode->next=head;
	head=newnode;
}	
void insert_end(struct node *traverse,struct node *newnode)
{
	newnode=(struct node *)malloc(sizeof(struct node));
	printf("\nenter the data of new node:");
	scanf("%d",&newnode->data);
	newnode->next=NULL;
	newnode->previous=NULL;
	traverse=head;
	while(traverse->next!=NULL)
	{
		traverse=traverse->next;
	}
	traverse->next=newnode;	
	newnode->previous=traverse;
}
void insert_location(struct node *traverse,struct node *newnode)
{
	int count=0,loc;
	struct node *ptr;
	printf("\nenter the location after that which you insert new node");
	scanf("%d",&loc);
	newnode=(struct node *)malloc(sizeof(struct node));
	printf("\nenter the data of new node:");
	scanf("%d",&newnode->data);
	newnode->next=NULL;
	newnode->previous=NULL;
	if(head==NULL)
	{
		head=newnode;
	}
	else
	traverse=head;
	while(traverse->next!=NULL && count!=loc)
	{
		ptr=traverse;
	    traverse=traverse->next;	
	    count++;
	}
	ptr->next=newnode;
	newnode->previous=ptr;
	newnode->next=traverse;
	traverse->previous=newnode;
}
void delete_beg(struct node *traverse)
{
	if(head==NULL)
	{
	printf("deletion not possible");
	}
	else
	{
	traverse=head;
	head=head->next;
	head->previous=NULL;
	printf("data of deleted node %d",traverse->data);
	free(traverse);
	}
}
void delete_end(struct node *traverse)
{
    struct node *ptr;
    traverse=head;
    while(traverse->next!=NULL)
    {
    	ptr=traverse;
    	traverse=traverse->next;
	}
    ptr->next=NULL;
    traverse->previous=NULL;
    printf("data of deleted node %d",traverse->data);
    free(traverse);
}
void delete_location(struct node *traverse)
{
	struct node *ptr,*forward;
	int count=1,loc;
	printf("\nenter the location of node that you want to delete");
	scanf("%d",&loc);
    traverse=head;
    while(traverse->next!=NULL&&count!=loc)
    {
    	ptr=traverse;
    	traverse=traverse->next;
    	count++;
	}
    forward=traverse->next;
    ptr->next=forward;
    forward->previous=ptr;
    printf("data of deleted node %d",traverse->data);
    free(traverse);
}