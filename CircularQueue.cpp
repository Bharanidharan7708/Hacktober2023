#include <iostream>
using namespace std;

const int max_size = 100;

int insertq(int queue[max_size], int *front, int *rear, int *data) {
    if ((*rear + 1) % max_size == *front) {
        return -1; 
    } else {
        if (*front == -1)
            *front = 0;
        *rear = (*rear + 1) % max_size;
        queue[*rear] = *data;
        return 1;
    }
}

int delq(int queue[max_size], int *front, int *rear, int *data) {
    if (*front == -1) {
        return -1; 
    } else {
        *data = queue[*front];
        if (*front == *rear) {
            *front = *rear = -1;
        } else {
            *front = (*front + 1) % max_size;
        }
        return 1;
    }
}

void display(int queue[max_size], int front, int rear) {
    if (front == -1) {
        cout << "Queue is Empty" << endl;
        return;
    }

    cout << "Queue elements: ";
    int i = front;
    do {
        cout << queue[i] << " ";
        i = (i + 1) % max_size;
    } while (i != (rear + 1) % max_size);
    cout << endl;
}

int main() {
    int queue[max_size], data;
    int front = -1, rear = -1, reply, option;

    while (true) {
        cout << "Enter 1 to insert an element\nEnter 2 to delete an element\nEnter 3 to display the elements\nEnter 4 to exit" << endl;
        cin >> option;
        switch (option) {
            case 1:
                cout << "Enter Number: ";
                cin >> data;
                reply = insertq(queue, &front, &rear, &data);
                if (reply == -1) {
                    cout << "Queue is Full" << endl;
                } else {
                    cout << data << " is inserted in the Queue" << endl;
                }
                break;
            case 2:
                reply = delq(queue, &front, &rear, &data);
                if (reply == -1) {
                    cout << "Queue is Empty" << endl;
                } else {
                    cout << "Deleted Number is: " << data << endl;
                }
                break;
            case 3:
                display(queue, front, rear);
                break;
            case 4:
                exit(0);
            default:
                cout << "Enter a valid choice" << endl;
        }
    }

    return 0;
}
