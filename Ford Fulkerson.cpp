#include <iostream>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

const int V = 100;  

int graph[V][V];    
int parent[V];      

int bfs(int source, int sink) {
    fill(parent, parent + V, -1);
    parent[source] = source;
    queue<pair<int, int>> q;
    q.push({source, INT_MAX});

    while (!q.empty()) {
        int cur = q.front().first;
        int flow = q.front().second;
        q.pop();

        for (int next = 0; next < V; next++) {
            if (parent[next] == -1 && graph[cur][next] > 0) {
                parent[next] = cur;
                int new_flow = min(flow, graph[cur][next]);
                if (next == sink) {
                    return new_flow;
                }
                q.push({next, new_flow});
            }
        }
    }
    return 0;
}

int fordFulkerson(int source, int sink) {
    int max_flow = 0;
    int new_flow;

    while ((new_flow = bfs(source, sink)) > 0) {
        int cur = sink;
        while (cur != source) {
            int prev = parent[cur];
            graph[prev][cur] -= new_flow;
            graph[cur][prev] += new_flow;
            cur = prev;
        }
        max_flow += new_flow;
    }
    return max_flow;
}

int main() {

    int source = 0;  
    int sink = 5;    

    int max_flow = fordFulkerson(source, sink);

    cout << "Maximum Flow: " << max_flow << endl;

    return 0;
}
