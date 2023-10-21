#include <iostream>
using namespace std;

const int MAX_SIZE = 100; 

class Queue {
private:
    int arr[MAX_SIZE];
    int front, rear;

public:
    Queue() {
        front = rear = -1; 
    }
    
    void enqueue(int value) {
        if (rear == MAX_SIZE - 1) {
            cout << "Queue is full. Cannot enqueue more elements." << endl;
            return;
        }
        if (front == -1)
            front = 0;
        arr[++rear] = value;
        cout << value << " has been enqueued." << endl;
    }

    void dequeue() {
        if (front == -1) {
            cout << "Queue is empty. Cannot dequeue from an empty queue." << endl;
            return;
        }
        cout << arr[front] << " has been dequeued." << endl;
        if (front == rear) {
            front = rear = -1;
        } else {
            front++;
        }
    }

    bool isEmpty() {
        return front == -1;
    }
};

int main() {
    Queue queue;
    int choice, value;

    while (true) {
        cout << "Queue Operations:" << endl;
        cout << "1. Enqueue" << endl;
        cout << "2. Dequeue" << endl;
        cout << "3. Quit" << endl;
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter a value to enqueue: ";
                cin >> value;
                queue.enqueue(value);
                break;
            case 2:
                queue.dequeue();
                break;
            case 3:
                exit(0);
            default:
                cout << "Invalid choice. Please try again." << endl;
        }
    }

    return 0;
}
