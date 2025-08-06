#include <iostream>
#include <chrono>
using namespace std;

int fib(int n) {
    return n <= 2 ? 1 : fib(n - 1) + fib(n - 2);
}

int main() {
    auto start = chrono::high_resolution_clock::now();
    cout << fib(30) << endl;
    auto end = chrono::high_resolution_clock::now();
    cout << "Time: " << chrono::duration<double>(end - start).count() << "s\n";
}

