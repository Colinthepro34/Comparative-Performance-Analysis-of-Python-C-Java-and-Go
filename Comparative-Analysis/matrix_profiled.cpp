#include <iostream>
#include <vector>
#include <chrono>
#include <random>
using namespace std;
int main() {
    const int n = 100;
    vector<vector<double>> A(n, vector<double>(n));
    vector<vector<double>> B(n, vector<double>(n));
    vector<vector<double>> C(n, vector<double>(n, 0.0));
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0, 1);
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) {
            A[i][j] = dis(gen);
            B[i][j] = dis(gen);
        }
    auto start = chrono::high_resolution_clock::now();
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            for (int k = 0; k < n; ++k)
                C[i][j] += A[i][k] * B[k][j];
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    cout << "Execution Time: " << elapsed.count() << "s\n";
    return 0;
}
