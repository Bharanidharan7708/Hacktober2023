#include <iostream>
#include <cstdlib>
#include <string>

using namespace std;

struct TreeNode {
    int data;
    TreeNode *left;
    TreeNode *right;
};

TreeNode *createNode(int new_data){
    struct TreeNode *new_node = new TreeNode;
    new_node -> data = new_data;
    new_node -> left = NULL;
    new_node -> right = NULL;
    return new_node;
}


void swapSubtrees(TreeNode *root) {
    if (root == NULL) {
        return;
    }

   
    TreeNode *temp = root -> left;
    root -> left = root -> right;
    root -> right = temp;

   
    swapSubtrees(root -> left);
    swapSubtrees(root -> right);
}


void Traversal(TreeNode *root) {
    if (root == NULL) {
        return;
    }
    Traversal(root -> left);
    cout << root -> data << " ";
    Traversal(root -> right);
}

int main() {
    TreeNode *root = createNode(1);
    root -> left = createNode(2);
    root -> right = createNode(3);
    root -> left -> left = createNode(4);
    root -> left -> left -> left = createNode(6);
    root -> left -> left -> left -> right = createNode(9);
   
    root -> right -> left = createNode(5);
    root -> right -> left -> left = createNode(7);
    root -> right -> left -> right = createNode(8);
    root -> right -> left -> right -> left = createNode(10);
    root -> right -> left -> right -> right = createNode(11);

    
    cout << "The elements in the input tree are: ";
    Traversal(root);
    cout << endl;

    
    swapSubtrees(root);

    
    cout << "The tree after left/right swapping of the nodes is: ";
    Traversal(root);
    cout << endl;

    return 0;
}

//TIME complexity - O(N)
//SPACE complexity - O(N) worst

