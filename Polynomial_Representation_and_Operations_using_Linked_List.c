#include<stdio.h>
#include<stdlib.h>
struct node
{
	int coeff;
	int degree;
	struct node *next;
};
struct node *head1=NULL,*head2=NULL,*head3=NULL;
struct node *createpoly1(struct node *nn,struct node *traverse1);
void display1(struct node *traverse1);
struct node *createpoly2(struct node *nn,struct node *traverse2);
void display2(struct node *traverse2);
struct node *addition(struct node *traverse1,struct node *traverse2,struct node *traverse3,struct node *nn);
void display3(struct node *traverse3);
int main()
{
   struct node *traverse1=NULL,*traverse2=NULL,*traverse3=NULL,*nn=NULL;
   printf("\nenter the data of first polynomial");
   head1=createpoly1(nn,traverse1);
   printf("\nfirst polynomial equation is:");
   display1(traverse1);
   printf("\nenter the data of second polynomial");
   head2=createpoly2(nn,traverse2);
   printf("\nsecond polynomial equation is:");
   display2(traverse2);
   head3=addition(traverse1,traverse2,traverse3,nn);
   printf("\nresultant polynomial equation is:");
   display3(traverse3);
}
struct node *createpoly1(struct node *nn,struct node *traverse1)
{
	int choice;
	do
	{
		nn=(struct node *)malloc(sizeof(struct node));
		printf("\nenter the coeffiecient:");
		scanf("%d",&nn->coeff);
		printf("\nenter the degree");
		scanf("%d",&nn->degree);
		nn->next=NULL;
		if(head1==NULL)
		{
			head1=nn;
			traverse1=head1;
		}
		else
		{
			traverse1->next=nn;
			traverse1=traverse1->next;
		}
	    printf("\nenter more node:1.yes 0.no");
	    scanf("%d",&choice);
	}
	while(choice);
	return head1;	
}
void display1(struct node *traverse1)
{
	traverse1=head1;
	while(traverse1->next!=NULL)
	{
		printf("%dx^%d+",traverse1->coeff,traverse1->degree);
		traverse1=traverse1->next;
	}
	printf("%dx^%d",traverse1->coeff,traverse1->degree);
}
struct node *createpoly2(struct node *nn,struct node *traverse2)
{
	int choice;
	do
	{
		nn=(struct node *)malloc(sizeof(struct node));
		printf("\nenter the coeffiecient:");
		scanf("%d",&nn->coeff);
		printf("\nenter the degree");
		scanf("%d",&nn->degree);
		nn->next=NULL;
		if(head2==NULL)
		{
			head2=nn;
			traverse2=head2;
		}
		else
		{
			traverse2->next=nn;
			traverse2=traverse2->next;
		}
	    printf("\nenter more node:1.yes 0.no");
	    scanf("%d",&choice);
	}
	while(choice);
	return head2;	
}
void display2(struct node *traverse2)
{
	traverse2=head2;
	while(traverse2->next!=NULL)
	{
		printf("%dx^%d+",traverse2->coeff,traverse2->degree);
		traverse2=traverse2->next;
	}
	printf("%dx^%d",traverse2->coeff,traverse2->degree);
}
struct node *addition(struct node *traverse1,struct node *traverse2,struct node *traverse3,struct node *nn)
{
   traverse1=head1;
   traverse2=head2;
   while(traverse1!=NULL&&traverse2!=NULL)
   {
   	if(traverse1->degree==traverse2->degree)
   	{
   	   nn=(struct node *)malloc(sizeof(struct node));
	   nn->coeff=traverse1->coeff+traverse2->coeff;
	   nn->degree=traverse1->degree;
	   nn->next==NULL;	
	   traverse1=traverse1->next;
	   traverse2=traverse2->next;
	   if(head3==NULL)
	   {
	   	head3=nn;
	   	traverse3=nn;
	   }
	   else
	   {
	   	traverse3->next=nn;
	   	traverse3=traverse3->next;
	   }
	}
	else if(traverse1->degree>traverse2->degree)
	{
	   nn=(struct node *)malloc(sizeof(struct node));
	   nn->coeff=traverse1->coeff;
	   nn->degree=traverse1->degree;
	   nn->next==NULL;	
	   traverse1=traverse1->next;
	   if(head3==NULL)
	   {
	   	head3=nn;
	   	traverse3=nn;
	   }
	   else
	   {
	   	traverse3->next=nn;
	   	traverse3=traverse3->next;
	   }
	}
	else if(traverse1->degree<traverse2->degree)
	{
	   nn=(struct node *)malloc(sizeof(struct node));
	   nn->coeff=traverse2->coeff;
	   nn->degree=traverse2->degree;
	   nn->next==NULL;
	   traverse2=traverse2->next;
	   if(head3==NULL)
	   {
	   	head3=nn;
	   	traverse3=nn;
	   }
	   else
	   {
	   	traverse3->next=nn;
	   	traverse3=traverse3->next;
	   }
	}
   }
   while(traverse1!=NULL)
   {
       nn=(struct node *)malloc(sizeof(struct node));
	   nn->coeff=traverse1->coeff;
	   nn->degree=traverse1->degree;
	   nn->next==NULL;	
	   traverse1=traverse1->next;
	   traverse3->next=nn;
	   traverse3=traverse3->next;
   }
   while(traverse2!=NULL)
   {
       nn=(struct node *)malloc(sizeof(struct node));
	   nn->coeff=traverse2->coeff;
	   nn->degree=traverse2->degree;
	   nn->next==NULL;	
	   traverse2=traverse2->next;
	   traverse3->next=nn;
	   traverse3=traverse3->next;
   }
   
 return head3;  	
}
void display3(struct node *traverse3)
{
	traverse3=head3;
	while(traverse3->next!=NULL)
	{
		printf("%dx^%d+",traverse3->coeff,traverse3->degree);
		traverse3=traverse3->next;
	}
    printf("%dx^%d",traverse3->coeff,traverse3->degree);
	
}