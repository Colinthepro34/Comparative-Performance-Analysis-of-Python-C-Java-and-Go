import time
def fib(n):
    return 1 if n <= 2 else fib(n-1) + fib(n-2)

start = time.time()
print(fib(30))
print("Time:", time.time() - start)
