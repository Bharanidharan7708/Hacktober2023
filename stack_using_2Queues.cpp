//Nikita12200
//implemenattion of stack using two Queues
#include <iostream>
#include <queue>
using namespace std;
template <typename T>
class stack
{
    queue<T> q1, q2;

public:
    void push(T x)
    {
        q1.push(x);
    }
    void pop()
    {
        //remove the last added element form q1
        //we have to move first n-1 element in q2
        //interchange the names of q1 and q2
        if (q1.empty())
            return;
        while (q1.size() > 1)
        {
            T element = q1.front();
            q2.push(element);
            q1.pop();
        }
        //removes the last element
        q1.pop();
        //swapping
        swap(q1, q2);
    }
    T top()
    {
        while (q1.size() > 1)
        {
            T element = q1.front();
            q2.push(element);
            q1.pop();
        }
        //1 element in q1
        T element = q1.front();
        q1.pop();
        q2.push(element);
        swap(q1, q2);
        return element;
    }
    int size()
    {
        return q1.size() + q2.size();
    }
    bool empty()
    {
        return size() == 0;
    }
};

int main()
{
    stack<int> s;
    int n;
    cin >> n;
    int a[n];
    for (int i = 0; i < n; i++)
    {
        cin >> a[i];
        s.push(a[i]);
    }
    while (!s.empty())
    {
        cout << s.top() << " ";
        s.pop();
    }
    return 0;
}
