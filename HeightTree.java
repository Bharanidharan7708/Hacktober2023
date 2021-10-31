package BinaryTree;

import java.util.Scanner;

public class HeightTree {

public static BinaryTreeNode<Integer> treeInputBetter(boolean isRoot,int parentData,boolean isLeft) {
		
		if(isRoot) {
		System.out.print("Enter Root Data: ");
		}
		else {
		if(isLeft) {
			System.out.print("Enter left child of "+parentData +" : ");
		}
		else {
			System.out.print("Enter right child of "+parentData+" : ");
		}
		}
		
		Scanner sc = new Scanner(System.in);
		int rootData=sc.nextInt();
		
		if(rootData == -1) {
			return null;
		}
		
		BinaryTreeNode<Integer> root = new BinaryTreeNode<Integer>(rootData);
		BinaryTreeNode<Integer> leftChild = treeInputBetter(false,rootData,true); 
		BinaryTreeNode<Integer> rightChild = treeInputBetter(false,rootData,false);
		root.left=leftChild;
		root.right=rightChild;
		return root;
		
	}
	

public static void printTree(BinaryTreeNode<Integer> root) {
	if(root == null) {
		return;
	}
	
	System.out.print(root.data + ":" );
	
	if(root.left != null) {
		System.out.print("L" + root.left.data + " ,");
	}
	if(root.right !=null) {
		System.out.print(" R"+root.right.data);
	}
	System.out.println();
	
	printTree(root.left);
	printTree(root.right);	
}


	
	public static int height(BinaryTreeNode<Integer> root) {
		
	if(root == null) {
		return 0;
	}
	
	return Math.max(height(root.left), height(root.right)) + 1 ;
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

		BinaryTreeNode<Integer> root = treeInputBetter(true, 0, true);
		
		System.out.println(height(root));
		
//		printTree(root);
		
	}

}
