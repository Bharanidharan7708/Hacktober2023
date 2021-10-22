#include<stdio.h>
#include<stdlib.h>
struct node
{
    int data;
    struct node * next;
}* top;
void push();
void pop();
void display();
int main()
{
    int n;
    top=NULL;
    printf("Enter the number of nodes \n");
    scanf("%d",&n);
    for(int i=1;i<=n;i++)
    {
        push();
    }
    printf("Stack:\n");
    display();
    pop();
    printf("\nUpdated Stack:\n");
    display();
    return 0;
}
void push()
{
    struct node *temp;
    temp=(struct node *)malloc(sizeof(struct node));
    printf("Enter data \n");
    scanf("%d",&temp->data);
    temp->next=NULL;
    if(top==NULL)
    {
        top=temp;
    }
    else
    {
        temp->next=top;
        top=temp;
    }
}
void pop()
{
    if(top==NULL)
    {
        printf("Underflow");
    }
    else
    {
         struct node *temp;
        printf("\n%d is popped",top->data);
        temp=top;
        top=top->next;
        temp=NULL;
        free(temp);
    }
}
void display()
{
    struct node *ptr=top;
    while(ptr->next!=NULL)
    {
        printf("%d\n",ptr->data);
        ptr=ptr->next;
    }
    printf("%d",ptr->data);
}
